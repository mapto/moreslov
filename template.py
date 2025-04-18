title_templ = "<h{level} id='{id}'>{content}</h{level}>"
span_templ = "<span id='{id}' class='value {type}' title='{title}'>{content}</span>"
tspan_templ = '<tspan x="0" y="{y}" font-size="smaller">{p}</tspan>'
value_link_templ = "<a href='{url}' id='{id}' class='value {type}' title='{title}' target='list'>{content}</a>"
list_link_templ = "<a href='{url}' id='{id}' class='link {type}' title='{title}' target='list'>{content}</a>"

text_templ = """<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="../../../style.css">
    <link rel="stylesheet" href="../values.css">
  </head>
<body><h1>{title}</h1>{body}</body></html>"""

table_templ = """<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" href="style.css">
  </head>
<body style="background: none;">{body}</body></html>"""

corpus_templ = """<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="../../style.css">
    <link rel="stylesheet" href="values.css">
  </head>
<body><h1>{title}</h1>{body}</body></html>"""

list_templ = """<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="{root_path}style.css">
  </head>
<body><h3>{title}</h3>{body}</body></html>"""

values_templ = """<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="../../style.css">
    <link rel="stylesheet" href="../../values-static.css">
    <link rel="stylesheet" href="values.css">
  </head>
<body>
  <h3>Analysis</h3>
  <div>
    <a href="map.html" target="fulltext">Texts vs Labels Heatmap</a><br/>
    <a href="map-condensed.html" target="fulltext">Corpora vs Values Heatmap</a><br/>
    <a href="keywords.svg" target="fulltext">Labels Venn Diagram</a>
  </div>
  <h3>{title}</h3>
    <form class="menu" id="vocab" action="/vocab" method="GET">
    <input type="hidden" name="stemmer" value="{stemmer}"/>
    <input type="hidden" name="vocab" value="{vocab}"/>
    {body}
    <input type="submit" id="submitVocab" value="{button}"/>
    </form>
</body></html>"""

venn_templ = {
    1: """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" height="100%" width="100%">
  <title>{title}</title>
  <svg x="50%" y="50%" overflow="visible" width="700" height="700">
    <g transform="translate(-350,-350)">
      <circle cx="37.5%" cy="37.5%" r="40%" style="fill:#aaffaa;fill-opacity:.5" />
      
      <text transform="translate(105,70)" width="20%" height="20%">
        <tspan x="0" y="-10" font-weight="bold">{a_name}</tspan>{a}
      </text>
    </g>
  </svg>
</svg>""",
    2: """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" height="100%" width="100%">
  <title>{title}</title>
  <svg x="50%" y="50%" overflow="visible" width="700" height="700">
    <g transform="translate(-350,-350)">
      <circle cx="37.5%" cy="37.5%" r="40%" style="fill:#aaffaa;fill-opacity:.5" />
      <circle cx="62.5%" cy="37.5%" r="40%" style="fill:#ffaaaa;fill-opacity:.5" />
      
      <text transform="translate(105,70)" width="20%" height="20%">
        <tspan x="0" y="-10" font-weight="bold">{a_name}</tspan>{a}
      </text>
      <text transform="translate(525,70)" width="20%" height="20%">
        <tspan x="0" y="-10" font-weight="bold">{b_name}</tspan>{b}
      </text>

      <text transform="translate(315,35)" width="20%" height="20%">
        {a_b}
      </text>
    </g>
  </svg>
</svg>""",
    3: """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" height="100%" width="100%">
  <title>{title}</title>
  <svg x="50%" y="50%" overflow="visible" width="700" height="700">
    <g transform="translate(-350,-350)">
      <g fill-opacity=".2" stroke="#000" stroke-width="2.4">
        <circle cx="37.5%" cy="37.5%" r="40%" style="fill:#aaffaa" />
        <circle cx="62.5%" cy="37.5%" r="40%" style="fill:#ffaaaa" />
        <circle cx="50%" cy="65%" r="40%" style="fill:#aaaaff" />
      </g>
      <text transform="translate(105,70)" width="20%" height="20%">
        <tspan x="0" y="-10" font-weight="bold">{a_name}</tspan>{a}
      </text>
      <text transform="translate(525,70)" width="20%" height="20%">
        <tspan x="0" y="-10" font-weight="bold">{b_name}</tspan>{b}
      </text>
      <text transform="translate(405,595)" width="20%" height="20%">
        <tspan x="0" y="-10" font-weight="bold">{c_name}</tspan>{c}
      </text>

      <text transform="translate(105,350)" width="20%" height="20%">
        {a_c}
      </text>
      <text transform="translate(535,350)" width="20%" height="20%">
        {b_c}
      </text>
      <text transform="translate(315,35)" width="20%" height="20%">
        {a_b}
      </text>

      <text transform="translate(315,210)" width="20%" height="20%">
        {a_b_c}
      </text>
    </g>
  </svg>
</svg>""",
    4: """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Source: https://en.wikipedia.org/wiki/Venn_diagram#/media/File:Venn's_four_ellipse_construction.svg -->
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" height="100%">
  <title>{title}</title>
	<defs>
		<ellipse id="a" rx="350" ry="230"/>
	</defs>
	<g fill-opacity=".2" stroke="#000" stroke-width="2.4">
		<use fill="#6fff05" transform="rotate(-40 960 -600)" xlink:href="#a"/>
		<use fill="#ff6405" transform="rotate(-40 650 -490)" xlink:href="#a"/>
		<use fill="#0525ff" transform="rotate(40 -180 800)" xlink:href="#a"/>
		<use fill="#1e1e1e" transform="rotate(40 -490 690)" xlink:href="#a"/>
	</g>

  <text transform="translate(255,70)" width="20%" height="20%">
    <tspan x="0" y="-10" font-weight="bold">{a_name}</tspan>{a}
  </text>
  <text transform="translate(600,70)" width="20%" height="20%">
    <tspan x="0" y="-10" font-weight="bold">{b_name}</tspan>{b}
  </text>
  <text transform="translate(80,260)" width="20%" height="20%">
    <tspan x="0" y="-10" font-weight="bold">{c_name}</tspan>{c}
  </text>
  <text transform="translate(780,260)" width="20%" height="20%">
    <tspan x="0" y="-10" font-weight="bold">{d_name}</tspan>{d}
  </text>

      <text transform="translate(425,65)" width="20%" height="20%">
        {a_b}
      </text>
      <text transform="translate(170,215)" width="20%" height="20%">
        {a_c}
      </text>
      <text transform="translate(700,420)" width="20%" height="20%">
        {a_d}
      </text>
      <text transform="translate(170,420)" width="20%" height="20%">
        {b_c}
      </text>
      <text transform="translate(700,215)" width="20%" height="20%">
        {b_d}
      </text>
      <text transform="translate(465,600)" width="20%" height="20%">
        {c_d}
      </text>

      <text transform="translate(245,290)" width="20%" height="20%">
        {a_b_c}
      </text>
      <text transform="translate(580,290)" width="20%" height="20%">
        {a_b_d}
      </text>
      <text transform="translate(560,530)" width="20%" height="20%">
        {a_c_d}
      </text>
      <text transform="translate(315,530)" width="20%" height="20%">
        {b_c_d}
      </text>

      <text transform="translate(400,380)" width="20%" height="20%">
        {a_b_c_d}
      </text>

</svg>""",
}

select_option_templ = '<option value="{value}" {default}>{label}</option>'

index_templ = """<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>moreslov - Syntactic Identification of Citations in Text Corpora</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="index.css">
    <script src="index.js"></script>
  </head>
<body onload="init()">
  <form class="menu">
    <div>
    <h1 class="title"><a href="https://github.com/umilISLab/moreever/">moreslov</a></h1>
    </div>
    <div>
      <input type="hidden" id="vocab-select" value="{vocab}"/>
    </div>
    <div>
      <label for="stemmer-select">Generalization:</label><br/>
      <!-- List defined in stemmers.py -->
      <select name="stemmer" id="stemmer-select">
        {stemmers}
      </select>
    </div>
    <div>
      <!-- TODO: load corpora dynamically -->
      <label for="corpus-select">Corpus:</label></br>
      <select name="corpus" id="corpus-select">
        {corpora}
      </select>
    </div>
    <br/>
    <div>
        <iframe name="list" id="list" src="{stem}/{vocab}/index.html"></iframe>
    </div>
  </form>
  <!-- TODO: generalise to first text in corpus list -->
  <iframe name="fulltext" id="fulltext" src="{text}"></iframe> 
  <div id="values-container">
      <iframe name="values" id="values" src="{stem}/{vocab}/values.html"></iframe> 
  </div>
  <footer>
    <a href="https://dllcm.unimi.it/"><img src="/logo-unimi.svg" height="100%"/></a>
    <div>
      developed at<br/>
      Università degli Studi di Milano<br/>
      <a href="https://dllcm.unimi.it/">https://dllcm.unimi.it/</a>
    </div>
  </footer>
</body></html>"""
