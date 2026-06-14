# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.resolve()))

project = "AI Accelerator: Analytics and Data Analysis"
author = "Jessica Nash"
copyright = "2026, Duke University"

extensions = [
    'myst_parser',
    'sphinx_design',
    'sphinx_copybutton',
    'sphinx_togglebutton',
    'sphinxcontrib.mermaid',
    '_extensions.ga_consent',
]

myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'html_image',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.venv', 'student-setup']
html_sidebars = {
    "index": ["root-sidebar-nav.html"],
    "**": ["sidebar-collapse.html", "sidebar-nav-bs.html"],
}

html_theme = "pydata_sphinx_theme"
html_static_path = ['_static', 'images']


html_logo = "images/ai-duke-transparent.png"
html_favicon = "images/favicon.png"

html_css_files = [

    "custom.css",
    "theme-duke-ai.css",

]

html_js_files = [


]

html_theme_options = {
    'logo': {

        'image_light': "images/ai-duke-transparent.png",
        'image_dark': "images/ai-duke-transparent.png",

    },
    'analytics': {
        'google_analytics_id': 'G-PCSTBS7XKG',
    },
    'icon_links': [
        {
            'name': 'Download PDF',
            'url': '../latex/ai-training-analytics-data-analysis.pdf',
            'icon': 'fa-solid fa-file-pdf',
        }
    ],
    'navbar_align': 'content',
    'navbar_center': [],
    'navbar_persistent': ['search-button-field'],
    'show_nav_level': 1,
    'show_toc_level': 3,
    'footer_start': ['site-footer'],
    'footer_center': [],
    'footer_end': [],
}

pygments_style = 'friendly'
pygments_dark_style = 'native'

latex_logo = 'images/duke_wordmark_navyblue_012169.pdf'
latex_engine = 'xelatex'
latex_documents = [
    (
        'index',
        'ai-training-analytics-data-analysis.tex',
        'AI Accelerator: Analytics and Data Analysis',
        'Jessica Nash',
        'howto',
    ),
]
