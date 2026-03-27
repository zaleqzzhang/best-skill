#!/usr/bin/env python3
"""
arXiv 论文通用搜索工具
支持关键词、主题、作者查询，可设置时间范围

依赖安装: pip install arxiv
"""

import arxiv
import argparse
from datetime import datetime, timedelta
from typing import Optional, List
import os


class ArxivSearcher:
    """arXiv 论文搜索器"""
    
    # 常用分类
    CATEGORIES = {
        "ai": "cs.AI",
        "ml": "cs.LG", 
        "nlp": "cs.CL",
        "cv": "cs.CV",
        "ir": "cs.IR",
        "se": "cs.SE",
        "db": "cs.DB",
        "net": "cs.NI",
        "crypto": "cs.CR",
        "robotics": "cs.RO",
        "stat": "stat.ML",
        "math": "math.*",
        "physics": "physics.*",
    }
    
    def __init__(self, download_dir: str = None):
        self.client = arxiv.Client()
        self.download_dir = download_dir or os.path.expanduser("~/Downloads/arxiv_papers")
    
    def build_query(
        self,
        keywords: Optional[List[str]] = None,
        title: Optional[str] = None,
        author: Optional[str] = None,
        abstract: Optional[str] = None,
        categories: Optional[List[str]] = None,
        arxiv_id: Optional[str] = None,
    ) -> str:
        """
        构建 arXiv 查询字符串
        
        arXiv 查询语法:
        - ti: 标题
        - au: 作者
        - abs: 摘要
        - cat: 分类
        - all: 所有字段
        """
        parts = []
        
        # arXiv ID 直接查询
        if arxiv_id:
            return arxiv_id
        
        # 关键词 (在所有字段搜索)
        if keywords:
            kw_parts = []
            for kw in keywords:
                if ' ' in kw:
                    kw_parts.append(f'all:"{kw}"')
                else:
                    kw_parts.append(f'all:{kw}')
            parts.append(f"({' AND '.join(kw_parts)})")
        
        # 标题搜索
        if title:
            if ' ' in title:
                parts.append(f'ti:"{title}"')
            else:
                parts.append(f'ti:{title}')
        
        # 作者搜索
        if author:
            # 支持多作者，用逗号分隔
            authors = [a.strip() for a in author.split(',')]
            au_parts = [f'au:"{a}"' if ' ' in a else f'au:{a}' for a in authors]
            parts.append(f"({' OR '.join(au_parts)})")
        
        # 摘要搜索
        if abstract:
            if ' ' in abstract:
                parts.append(f'abs:"{abstract}"')
            else:
                parts.append(f'abs:{abstract}')
        
        # 分类过滤
        if categories:
            resolved_cats = []
            for cat in categories:
                cat = cat.strip().lower()
                if cat in self.CATEGORIES:
                    resolved_cats.append(self.CATEGORIES[cat])
                else:
                    resolved_cats.append(cat)
            cat_parts = [f'cat:{c}' for c in resolved_cats]
            parts.append(f"({' OR '.join(cat_parts)})")
        
        return ' AND '.join(parts) if parts else 'all:*'
    
    def search(
        self,
        keywords: Optional[List[str]] = None,
        title: Optional[str] = None,
        author: Optional[str] = None,
        abstract: Optional[str] = None,
        categories: Optional[List[str]] = None,
        arxiv_id: Optional[str] = None,
        days: int = 365,
        max_results: int = 50,
        sort_by: str = "submitted",
    ) -> List[dict]:
        """
        搜索论文
        
        Args:
            keywords: 关键词列表
            title: 标题关键词
            author: 作者名 (多作者用逗号分隔)
            abstract: 摘要关键词
            categories: 分类列表 (如 cs.AI, cs.LG 或简写 ai, ml)
            arxiv_id: arXiv ID (直接获取特定论文)
            days: 时间范围 (天数，默认365天=1年)
            max_results: 最大返回数量
            sort_by: 排序方式 (submitted/relevance/updated)
        
        Returns:
            论文列表
        """
        query = self.build_query(
            keywords=keywords,
            title=title,
            author=author,
            abstract=abstract,
            categories=categories,
            arxiv_id=arxiv_id,
        )
        
        print(f"查询语句: {query}")
        print(f"时间范围: 最近 {days} 天")
        print("-" * 60)
        
        sort_mapping = {
            "submitted": arxiv.SortCriterion.SubmittedDate,
            "relevance": arxiv.SortCriterion.Relevance,
            "updated": arxiv.SortCriterion.LastUpdatedDate,
        }
        
        search = arxiv.Search(
            query=query,
            max_results=max_results * 2,  # 多获取一些用于时间过滤
            sort_by=sort_mapping.get(sort_by, arxiv.SortCriterion.SubmittedDate),
            sort_order=arxiv.SortOrder.Descending,
        )
        
        cutoff_date = datetime.now() - timedelta(days=days)
        results = []
        
        for paper in self.client.results(search):
            # 时间过滤
            if paper.published.replace(tzinfo=None) < cutoff_date:
                continue
            
            results.append({
                "id": paper.entry_id.split("/")[-1],
                "title": paper.title.replace('\n', ' '),
                "authors": [a.name for a in paper.authors],
                "summary": paper.summary.replace('\n', ' '),
                "published": paper.published.strftime("%Y-%m-%d"),
                "updated": paper.updated.strftime("%Y-%m-%d"),
                "categories": paper.categories,
                "pdf_url": paper.pdf_url,
                "arxiv_url": paper.entry_id,
                "_paper": paper,
            })
            
            if len(results) >= max_results:
                break
        
        return results
    
    def display(self, results: List[dict], verbose: bool = False):
        """显示搜索结果"""
        if not results:
            print("\n未找到符合条件的论文")
            return
        
        print(f"\n{'='*80}")
        print(f"共找到 {len(results)} 篇论文")
        print(f"{'='*80}\n")
        
        for i, paper in enumerate(results, 1):
            print(f"[{i}] {paper['title']}")
            
            # 作者
            authors = ', '.join(paper['authors'][:4])
            if len(paper['authors']) > 4:
                authors += ' et al.'
            print(f"    作者: {authors}")
            
            # 日期和分类
            cats = ', '.join(paper['categories'][:3])
            print(f"    发布: {paper['published']} | 分类: {cats}")
            
            # 链接
            print(f"    链接: {paper['arxiv_url']}")
            print(f"    PDF: {paper['pdf_url']}")
            
            # 摘要
            if verbose:
                abstract = paper['summary'][:400] + '...' if len(paper['summary']) > 400 else paper['summary']
                print(f"    摘要: {abstract}")
            
            print()
    
    def download(self, results: List[dict], indices: Optional[List[int]] = None):
        """下载论文 PDF"""
        os.makedirs(self.download_dir, exist_ok=True)
        
        if indices is None:
            to_download = results
        else:
            to_download = [results[i-1] for i in indices if 0 < i <= len(results)]
        
        for paper in to_download:
            try:
                arxiv_paper = paper["_paper"]
                safe_id = paper["id"].replace("/", "_")
                filepath = os.path.join(self.download_dir, f"{safe_id}.pdf")
                arxiv_paper.download_pdf(dirpath=self.download_dir, filename=f"{safe_id}.pdf")
                print(f"已下载: {filepath}")
            except Exception as e:
                print(f"下载失败 [{paper['id']}]: {e}")
    
    def export_markdown(self, results: List[dict], output_file: str = None):
        """导出为 Markdown 格式"""
        if not output_file:
            output_file = os.path.join(self.download_dir, f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        lines = [
            f"# arXiv 论文搜索结果",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**论文数量**: {len(results)} 篇",
            "",
            "---",
            "",
        ]
        
        for i, paper in enumerate(results, 1):
            authors = ', '.join(paper['authors'][:4])
            if len(paper['authors']) > 4:
                authors += ' et al.'
            
            lines.extend([
                f"## {i}. {paper['title']}",
                "",
                f"- **作者**: {authors}",
                f"- **发布日期**: {paper['published']}",
                f"- **分类**: {', '.join(paper['categories'][:3])}",
                f"- **arXiv**: [{paper['id']}]({paper['arxiv_url']})",
                f"- **PDF**: [下载]({paper['pdf_url']})",
                "",
                f"**摘要**: {paper['summary'][:500]}{'...' if len(paper['summary']) > 500 else ''}",
                "",
                "---",
                "",
            ])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"已导出: {output_file}")
        return output_file


def main():
    parser = argparse.ArgumentParser(
        description="arXiv 论文搜索工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 按关键词搜索 (默认最近1年)
  python arxiv_search.py -k "retrieval augmented generation" "RAG"
  
  # 按作者搜索
  python arxiv_search.py -a "Yann LeCun"
  
  # 按标题搜索
  python arxiv_search.py -t "transformer"
  
  # 限定分类 (支持简写: ai, ml, nlp, cv, ir 等)
  python arxiv_search.py -k "LLM" -c cs.CL cs.AI
  python arxiv_search.py -k "LLM" -c nlp ai
  
  # 设置时间范围
  python arxiv_search.py -k "GPT" --days 30   # 最近30天
  python arxiv_search.py -k "GPT" --days 7    # 最近1周
  
  # 组合查询
  python arxiv_search.py -k "RAG" -a "OpenAI" -c ai --days 180
  
  # 显示详细摘要
  python arxiv_search.py -k "RAG" -v
  
  # 导出为 Markdown
  python arxiv_search.py -k "RAG" --export
  
  # 下载论文
  python arxiv_search.py -k "RAG" --download 1,2,3
  python arxiv_search.py -k "RAG" --download all

常用分类简写:
  ai=cs.AI  ml=cs.LG  nlp=cs.CL  cv=cs.CV  ir=cs.IR
  se=cs.SE  db=cs.DB  crypto=cs.CR  robotics=cs.RO
        """
    )
    
    # 搜索条件
    parser.add_argument('-k', '--keywords', nargs='+', help='关键词 (支持多个)')
    parser.add_argument('-t', '--title', help='标题关键词')
    parser.add_argument('-a', '--author', help='作者名 (多作者用逗号分隔)')
    parser.add_argument('-b', '--abstract', help='摘要关键词')
    parser.add_argument('-c', '--categories', nargs='+', help='分类 (如 cs.AI 或简写 ai)')
    parser.add_argument('-i', '--id', help='arXiv ID (直接获取特定论文)')
    
    # 时间和数量
    parser.add_argument('--days', type=int, default=365, help='时间范围 (天数, 默认365)')
    parser.add_argument('-n', '--num', type=int, default=20, help='返回数量 (默认20)')
    parser.add_argument('-s', '--sort', choices=['submitted', 'relevance', 'updated'], 
                        default='submitted', help='排序方式 (默认submitted)')
    
    # 输出选项
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细摘要')
    parser.add_argument('--export', action='store_true', help='导出为 Markdown')
    parser.add_argument('--download', help='下载论文 (序号如 1,2,3 或 all)')
    
    args = parser.parse_args()
    
    # 至少需要一个搜索条件
    if not any([args.keywords, args.title, args.author, args.abstract, args.categories, args.id]):
        parser.print_help()
        print("\n错误: 请至少提供一个搜索条件")
        return
    
    searcher = ArxivSearcher()
    
    # 执行搜索
    results = searcher.search(
        keywords=args.keywords,
        title=args.title,
        author=args.author,
        abstract=args.abstract,
        categories=args.categories,
        arxiv_id=args.id,
        days=args.days,
        max_results=args.num,
        sort_by=args.sort,
    )
    
    # 显示结果
    searcher.display(results, verbose=args.verbose)
    
    # 导出
    if args.export and results:
        searcher.export_markdown(results)
    
    # 下载
    if args.download and results:
        if args.download.lower() == 'all':
            searcher.download(results)
        else:
            indices = [int(i.strip()) for i in args.download.split(',') if i.strip().isdigit()]
            searcher.download(results, indices)


if __name__ == "__main__":
    main()
