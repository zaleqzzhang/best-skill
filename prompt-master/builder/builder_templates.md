{
  "_meta": {
    "module": "builder",
    "role": "构建引擎：接收focused_json(来自上游聚焦层) -> 字段填充 -> 编译器 -> 平台原生格式。不负责聚焦逻辑。",
    "version": "v5.3"
  },
  "fields": {
    "image": {
      "P0_core": [
        {
          "key": "subject",
          "label": "主体",
          "required": true
        },
        {
          "key": "style",
          "label": "风格",
          "required": true
        },
        {
          "key": "platform",
          "label": "平台",
          "required": true
        }
      ],
      "P1_extend": [
        "composition",
        "lighting",
        "color",
        "mood",
        "camera",
        "quality"
      ]
    },
    "video": {
      "P0_core": [
        {
          "key": "subject",
          "label": "主体",
          "required": true
        },
        {
          "key": "motion",
          "label": "运动方式",
          "required": true
        },
        {
          "key": "platform",
          "label": "平台",
          "required": true
        }
      ],
      "P1_extend": [
        "camera_move",
        "environment",
        "lighting",
        "mood",
        "duration"
      ]
    }
  },
  "image_templates": {
    "A_photorealistic": {
      "structure": "{subject} {setting}, {lighting}, {camera} {quality}",
      "cache_brush": [
        "raw photo",
        "ungraded",
        "natural lighting",
        "35mm film grain",
        "shot on Canon EOS R5",
        "f/1.8 bokeh"
      ],
      "cache_texture": [
        "skin pore detail",
        "fabric weave",
        "water droplets",
        "dust particles",
        "subsurface scattering",
        "8k resolution"
      ]
    },
    "B_illustration": {
      "structure": "{subject} in {style} style, {composition} background, {mood}",
      "cache_brush": [
        "flat color",
        "clean lines",
        "bold outlines",
        "vector-style",
        "cel shaded",
        "digital painting"
      ],
      "cache_texture": [
        "paper texture",
        "canvas grain",
        "ink bleed effect",
        "watercolor bloom",
        "pencil strokes"
      ]
    },
    "C_cinematic": {
      "structure": "cinematic shot of {subject}, {camera_movement}, {lighting_drama}, {atmosphere}",
      "cache_brush": [
        "anamorphic lens flare",
        "film grain",
        "color graded",
        "depth of field",
        "dramatic lighting",
        "teal & orange"
      ],
      "cache_texture": [
        "bokeh circles",
        "lens distortion",
        "vignette",
        "chromatic aberration",
        "light leaks"
      ]
    },
    "D_abstract": {
      "structure": "abstract {subject} composition, {color_palette}, {texture_desc}, {mood}",
      "cache_brush": [
        "fluid shapes",
        "organic forms",
        "geometric patterns",
        "gradient mesh",
        "particle swarm",
        "ink diffusion"
      ],
      "cache_texture": [
        "iridescent",
        "translucent",
        "glowing edges",
        "fractal details",
        "smoke wisps",
        "holographic"
      ]
    }
  },
  "video_templates": {
    "A_cinematic_film": {
      "structure": "{subject}. {camera_move} as it {motion_desc}. {env_light}. Duration: {dur}s.",
      "cache_render": [
        "cinematic",
        "film quality",
        "movie-like",
        "professional grade",
        "blockbuster",
        "IMAX feel"
      ],
      "cache_extra": [
        "anamorphic",
        "color grading",
        "dramatic score",
        "slow motion",
        "wide angle",
        "epic scale"
      ]
    },
    "B_dynamic_commercial": {
      "structure": "{motion_desc} of {subject}. Fast cuts with {camera_move}. {env_light}. Duration: {dur}s.",
      "cache_render": [
        "high energy",
        "dynamic",
        "vibrant",
        "commercial quality",
        "polished",
        "advertising style"
      ],
      "cache_extra": [
        "product showcase",
        "lifestyle",
        "bright colors",
        "clean background",
        "upbeat rhythm",
        "quick cuts"
      ]
    },
    "C_artistic_experimental": {
      "structure": "{artistic_style} depiction of {subject} {motion_desc}. Dreamlike {camera_move}. Duration: {dur}s.",
      "cache_render": [
        "artistic",
        "experimental",
        "avant-garde",
        "creative",
        "unique vision",
        "gallery piece"
      ],
      "cache_extra": [
        "surreal transitions",
        "morphing effects",
        "abstract visuals",
        "symbolic imagery",
        "non-linear"
      ]
    },
    "D_documentary_realistic": {
      "structure": "Documentary footage of {subject} {motion_desc}. Handheld {camera_move}. Natural {env_light}. Duration: {dur}s.",
      "cache_render": [
        "documentary",
        "realistic",
        "authentic",
        "candid",
        "real-life",
        "journalistic"
      ],
      "cache_extra": [
        "fly on the wall",
        "observational",
        "ambient sound",
        "natural light",
        "no staging",
        "raw feel"
      ]
    }
  }
}