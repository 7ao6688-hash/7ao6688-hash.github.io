"""Build index.html (the home page): the warm, map-product version of the home page (direction chosen from Felt). Reuses the case
list and shared sections from build_v2.py, with its own header, hero and stylesheet."""
import runpy
from pathlib import Path

here = Path(__file__).parent
v2 = runpy.run_path(str(here / "build_v2.py"))   # also refreshes v2.html; harmless
section, script, footer = v2["section"], v2["script"], v2["footer"]

# Natural-colour covers for the two scenes that were false colour in v2
COVERS = {"valencia": "tiles3/valencia.webp", "chlorophyll": "tiles3/chlorophyll.webp", "lidar": "tiles3/lidar.webp"}
cases = [(s, t, COVERS.get(s, img), lab, title, key) for s, t, img, fit, lab, title, key in v2["CASES"]]

tiles = "\n".join(f"""        <a class="case t-{slug}" href="case/{slug}.html" data-tags="{tags}">
          <div class="ph"><img src="assets/{img}" alt="" loading="lazy"></div>
          <div class="cap">
            <p class="label" data-zh="{lab[1]}">{lab[0]}</p>
            <h3 data-zh="{title[1]}">{title[0]}</h3>
            <p class="key" data-zh="{key[1]}">{key[0]}</p>
          </div>
        </a>""" for slug, tags, img, lab, title, key in cases)

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Xiaoqiao Liu, Earth observation</title>
<meta name="description" content="Remote sensing and GIS analyst: flood mapping, InSAR ground deformation, forest carbon, urban heat and GIS automation from satellite radar, LiDAR and optical data.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">
<link rel="stylesheet" href="assets/v3.css?v=4">
<link rel="icon" href="assets/icon.svg" type="image/svg+xml">
<meta property="og:title" content="Xiaoqiao Liu, Earth observation">
<meta property="og:description" content="Flood mapping, InSAR ground deformation, forest carbon and urban heat from satellite radar, LiDAR and optical data.">
<meta property="og:image" content="https://7ao6688-hash.github.io/assets/og.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
</head>
<body>
"""

BODY = f"""<div class="coordbar" aria-hidden="true"><div class="wrap">
  <span><i>LAT</i> 39.40° N</span><span><i>LON</i> 0.38° W</span><span><i>SENSOR</i> Landsat 8</span><span><i>DATE</i> 30 Oct 2024</span>
  <span class="r"><i>CRS</i> EPSG:4326</span>
</div></div>
<header class="top">
  <div class="wrap">
    <a class="brand" href="#top">Xiaoqiao Liu</a>
    <nav class="links" aria-label="Sections">
      <a href="#work" data-zh="案例">Work</a>
      <a href="#lab" data-zh="互动工具">Lab</a>
      <a href="#services" data-zh="服务">Services</a>
      <a href="#about" data-zh="关于我">About</a>
      <button class="lang" id="lang" type="button" aria-label="Switch language">中文</button>
      <a class="btn primary small" href="#contact" data-zh="联系我">Get in touch</a>
    </nav>
  </div>
</header>

<main id="top">
  <div class="hero">
    <div class="wrap">
      <div class="hero-text">
        <p class="eyebrow" data-zh="遥感与 GIS 分析">Remote sensing &amp; GIS analysis</p>
        <h1 data-zh="把卫星数据变成可以据此决策的答案">Satellite data turned into answers you can act on</h1>
        <p class="lede" data-zh="我用雷达、LiDAR 和光学卫星影像绘制洪水范围、测量地表形变、估算森林碳储量、定位城市热点。每个结果都附带地图、可直接使用的数据和一份简明报告。">I map floods, measure ground movement, estimate forest carbon and find urban hot spots from radar, LiDAR and optical imagery. Every result comes with maps, ready-to-use data and a short plain-language report.</p>
        <div class="cta">
          <a class="btn primary" href="#contact" data-zh="咨询项目">Discuss a project</a>
          <a class="btn" href="#work" data-zh="查看案例">See the work</a>
        </div>
      </div>
    </div>
    <figure class="hero-img" aria-label="Before and after comparison of the October 2024 Valencia flood">
      <div class="stage" id="stage" tabindex="0" role="slider" aria-label="Before/after divider" aria-valuemin="0" aria-valuemax="100" aria-valuenow="55">
        <img draggable="false" id="img-before" src="assets/slider-optical-pre.webp" alt="Landsat image before the flood">
        <img draggable="false" id="img-after" class="after" src="assets/slider-optical-post.webp" alt="Landsat image the day after the flood">
        <span class="tag-date l" id="date-before">28 Sep</span>
        <span class="tag-date r" id="date-after">30 Oct</span>
        <div class="handle"></div>
      </div>
      <input class="sr" type="range" id="cut" min="0" max="100" value="55" aria-label="Move the divider between before and after">
      <div class="note n1" aria-hidden="true">
        <p class="note-title" data-zh="瓦伦西亚洪水，2024 年 10 月">Valencia flood, October 2024</p>
        <p class="note-row"><span class="dot water"></span><span data-zh="积水，10 月 30 日">Standing water, 30 Oct</span><b>67 km²</b></p>
        <p class="note-row"><span class="dot radar"></span><span data-zh="雷达：11 月 1 日仍被淹">Still flooded on radar, 1 Nov</span><b>42 km²</b></p>
        <p class="note-row"><span class="dot dry"></span><span data-zh="11 月 6 日剩余">Left by 6 Nov</span><b>14 km²</b></p>
      </div>
      <figcaption class="note n2">
        <span class="avatar" aria-hidden="true">XL</span>
        <div>
          <p id="compare-cap" data-zh="瓦伦西亚，2024 年 10 月。Landsat 8 真彩色：洪水后一天，阿尔武费拉潟湖周边的农田被褐色洪水覆盖。左右拖动影像对比洪水前后。">Valencia, October 2024. Landsat 8 true colour: the day after the flood, brown water covers the fields around the Albufera lagoon. Drag across the image to compare.</p>
          <div class="seg" role="group" aria-label="Sensor">
            <button type="button" id="mode-optical" aria-pressed="true" data-zh="光学">Optical</button>
            <button type="button" id="mode-radar" aria-pressed="false" data-zh="雷达">Radar</button>
          </div>
        </div>
      </figcaption>
    </figure>
  </div>

  <section id="work">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow" data-zh="作品">Work</p><h2 data-zh="八个研究项目，代码全部公开">Eight research projects, all with open code</h2></div>
        <p data-zh="每个项目都有公开的代码、测试和结果。点任意一张图看完整案例。">Each project has public code, tests and results. Open any image for the full case study.</p>
      </div>
      <div class="filters" role="group" aria-label="Filter case studies">
        <button class="chip" type="button" data-filter="all" aria-pressed="true" data-zh="全部">All</button>
        <button class="chip" type="button" data-filter="radar" aria-pressed="false" data-zh="雷达">Radar</button>
        <button class="chip" type="button" data-filter="optical" aria-pressed="false" data-zh="光学 / 热红外">Optical &amp; thermal</button>
        <button class="chip" type="button" data-filter="lidar" aria-pressed="false">LiDAR</button>
        <button class="chip" type="button" data-filter="gis" aria-pressed="false" data-zh="GIS 与水资源">GIS &amp; water</button>
      </div>
      <div class="mosaic" id="cases">
{tiles}
      </div>
    </div>
  </section>

{section("lab")}
{section("services")}
{section("process")}
{section("about")}
{section("contact")}</main>

{footer}
"""

BODY = BODY.replace('href="#case-valencia"', 'href="case/valencia.html"').replace('href="#case-insar"', 'href="case/earthquakes.html"') \
           .replace('href="#case-wildfire"', 'href="case/wildfire.html"').replace('href="#case-glasgow"', 'href="case/glasgow.html"') \
           .replace('href="#case-sites"', 'href="case/sites.html"')
assert "#case-" not in BODY

# In Chinese, case links open the Chinese case pages (the page script's toggle sets <html lang>).
CASE_LANG = """<script>
(() => {
  const links = [...document.querySelectorAll('a[href^="case/"]')];
  links.forEach(a => { a.dataset.en = a.getAttribute("href"); });
  const sync = () => {
    const zh = document.documentElement.lang.startsWith("zh");
    links.forEach(a => a.setAttribute("href", zh ? a.dataset.en.replace(".html", "-zh.html") : a.dataset.en));
  };
  new MutationObserver(sync).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  sync();
})();
</script>
"""
html = HEAD + BODY + script + CASE_LANG + "</body>\n</html>\n"   # script includes the lab.js tag and the optical default
(here / "index.html").write_text(html, encoding="utf-8")
print(f"index.html written ({len(html) // 1024} KB)")
