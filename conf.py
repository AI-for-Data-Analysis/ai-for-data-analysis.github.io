# Configuration file for the Sphinx documentation builder.

project = "AI Training for Analytics and Data Analysis"
author = "Jessica Nash"
copyright = "2026, Duke University Office of Information Technology"

extensions = [
    'myst_parser',
    'sphinx_design',
    'sphinx_copybutton',
    'sphinx_togglebutton',
    'sphinxcontrib.mermaid',
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
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.venv']
html_sidebars = {
    "index": ["root-sidebar-nav.html"],
    "**": ["sidebar-collapse.html", "sidebar-nav-bs.html"],
}

html_theme = "pydata_sphinx_theme"
html_static_path = ['_static']


html_logo = "images/oit-logo.svg"

html_css_files = [

    "custom.css",

]

html_js_files = [


]

html_theme_options = {
    'logo': {

        'image_light': "images/oit-logo.svg",
        'image_dark': "images/oit-logo.svg",

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
}

pygments_style = 'friendly'
pygments_dark_style = 'native'

latex_logo = 'images/duke_wordmark_navyblue_012169.pdf'
latex_engine = 'xelatex'
latex_documents = [
    (
        'index',
        'ai-training-analytics-data-analysis.tex',
        'AI Training for Analytics and Data Analysis',
        'Jessica Nash',
        'howto',
    ),
]
