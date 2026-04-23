"""
文件解析模块
支持 txt / pdf / epub / docx 格式，提取纯文本内容。
"""
import io
from pathlib import Path
from typing import Optional

import chardet
from loguru import logger


ALLOWED_EXTENSIONS = {".txt", ".pdf", ".epub", ".mobi", ".docx"}


class FileParseError(Exception):
    """文件解析异常。"""

    def __init__(self, message: str, detail: Optional[str] = None):
        self.message = message
        self.detail = detail
        super().__init__(message)


def detect_encoding(raw_bytes: bytes) -> str:
    """检测文件编码，按优先级尝试。"""
    result = chardet.detect(raw_bytes)
    encoding = result.get("encoding", "utf-8") or "utf-8"
    logger.debug(f"检测到编码: {encoding} (置信度: {result.get('confidence', 0):.2f})")
    return encoding


def parse_txt(content: bytes) -> str:
    """解析纯文本文件。"""
    encoding = detect_encoding(content)
    for enc in [encoding, "utf-8", "gbk", "gb2312", "big5"]:
        try:
            return content.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    raise FileParseError("无法解码文本文件", detail=f"尝试编码: {encoding}, utf-8, gbk, gb2312, big5")


def parse_pdf(content: bytes) -> str:
    """解析 PDF 文件，提取全部文本。"""
    try:
        from PyPDF2 import PdfReader
    except ImportError as e:
        raise FileParseError("缺少 PDF 解析依赖", detail=str(e))

    try:
        reader = PdfReader(io.BytesIO(content))
        texts = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                texts.append(text.strip())
            else:
                logger.warning(f"PDF 第 {i + 1} 页未提取到文本")
        if not texts:
            raise FileParseError("PDF 文件未提取到任何文本内容")
        return "\n\n".join(texts)
    except FileParseError:
        raise
    except Exception as e:
        raise FileParseError("PDF 解析失败", detail=str(e))


def parse_epub(content: bytes) -> str:
    """解析 EPUB 电子书，提取章节文本。"""
    try:
        import ebooklib
        from ebooklib import epub
        from html.parser import HTMLParser
    except ImportError as e:
        raise FileParseError("缺少 EPUB 解析依赖", detail=str(e))

    class HTMLTextExtractor(HTMLParser):
        """简单 HTML 文本提取器。"""

        def __init__(self):
            super().__init__()
            self.texts: list[str] = []
            self._skip = False

        def handle_starttag(self, tag, attrs):
            if tag in ("script", "style"):
                self._skip = True

        def handle_endtag(self, tag):
            if tag in ("script", "style"):
                self._skip = False
            if tag in ("p", "div", "br", "h1", "h2", "h3", "h4", "h5", "h6", "li"):
                self.texts.append("\n")

        def handle_data(self, data):
            if not self._skip:
                self.texts.append(data)

        def get_text(self) -> str:
            return "".join(self.texts).strip()

    try:
        book = epub.read_epub(io.BytesIO(content))
        texts = []
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            html_content = item.get_content().decode("utf-8", errors="ignore")
            extractor = HTMLTextExtractor()
            extractor.feed(html_content)
            text = extractor.get_text()
            if text.strip():
                texts.append(text.strip())
        if not texts:
            raise FileParseError("EPUB 文件未提取到任何文本内容")
        return "\n\n".join(texts)
    except FileParseError:
        raise
    except Exception as e:
        raise FileParseError("EPUB 解析失败", detail=str(e))


def parse_docx(content: bytes) -> str:
    """解析 Word 文档。"""
    try:
        from docx import Document
    except ImportError as e:
        raise FileParseError("缺少 DOCX 解析依赖", detail=str(e))

    try:
        doc = Document(io.BytesIO(content))
        texts = [para.text for para in doc.paragraphs if para.text.strip()]
        if not texts:
            raise FileParseError("DOCX 文件未提取到任何文本内容")
        return "\n\n".join(texts)
    except FileParseError:
        raise
    except Exception as e:
        raise FileParseError("DOCX 解析失败", detail=str(e))


def parse_file(filename: str, content: bytes) -> str:
    """
    根据文件扩展名选择解析器，提取纯文本。

    Args:
        filename: 原始文件名
        content: 文件二进制内容

    Returns:
        提取的纯文本字符串

    Raises:
        FileParseError: 文件格式不支持或解析失败
    """
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise FileParseError(
            f"不支持的文件格式: {ext}",
            detail=f"支持的格式: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    logger.info(f"开始解析文件: {filename} (格式: {ext}, 大小: {len(content)} bytes)")

    parsers = {
        ".txt": parse_txt,
        ".pdf": parse_pdf,
        ".epub": parse_epub,
        ".docx": parse_docx,
        ".mobi": lambda c: parse_txt(c),  # mobi 简单回退到文本解析
    }

    parser = parsers.get(ext)
    if parser is None:
        raise FileParseError(f"未找到 {ext} 格式的解析器")

    text = parser(content)
    logger.info(f"文件解析完成: {len(text)} 字符")
    return text
