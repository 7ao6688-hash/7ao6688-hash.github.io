"""Build v2.html: the imagery-led version of the home page. Reuses the content of page.html (services, lab,
process, about, contact, scripts) and replaces the header, hero and case grid with full-bleed imagery."""
import re
from pathlib import Path

here = Path(__file__).parent
src = (here / "page.html").read_text(encoding="utf-8").split("<!--BODY-->", 1)[1]


def section(sid):
    m = re.search(r'  <section id="%s">.*?\n  </section>\n' % sid, src, re.S)
    assert m, sid
    return m.group(0)


script = src[src.index("<script>"):]
footer = re.search(r"<footer>.*?</footer>\n", src, re.S).group(0)

CASES = [
    # slug, tags, image, fit, label (en, zh), title (en, zh), key (en, zh)
    ("valencia", "radar optical", "tiles/valencia.webp", "",
     ("Flood mapping, Valencia, 2024", "洪水制图，瓦伦西亚，2024"),
     ("Valencia DANA flood", "瓦伦西亚 DANA 洪水"),
     ("67 km² of standing water the day after; radar tracks it draining to 14 km² a week later.",
      "洪水后一天积水 67 km²；雷达跟踪到一周后退至 14 km²。")),
    ("earthquakes", "radar", "tiles/earthquakes.webp", "",
     ("InSAR, Türkiye and Morocco, 2023", "InSAR，土耳其与摩洛哥，2023"),
     ("Earthquake ground deformation", "地震引起的地表形变"),
     ("About 74 cm of line-of-sight change across 10 km of the Kahramanmaraş rupture.",
      "卡赫拉曼马拉什破裂带 10 km 范围内视线向位移变化约 74 cm。")),
    ("wildfire", "optical", "tiles/wildfire.webp", "",
     ("Forest carbon, California, 2020", "森林碳储量，美国加州，2020"),
     ("Wildfire carbon loss", "野火碳损失"),
     ("6.8 million tonnes of carbon; 10% of the area burned hot and caused 58% of the loss.",
      "约 680 万吨碳；10% 的高强度火烧区贡献了 58% 的损失。")),
    ("glasgow", "optical", "tiles/glasgow.webp", "",
     ("Urban heat, Glasgow, 2019", "城市热岛，格拉斯哥，2019"),
     ("Where greening cools Glasgow", "格拉斯哥绿化降温优先区"),
     ("25.5 km² of hot, bare built-up land flagged first for street trees and green roofs.",
      "25.5 km² 炎热且缺少绿化的建成区被列为优先区。")),
    ("spain", "gis", "tiles/spain.webp", "",
     ("Water resources, Spain", "水资源，西班牙"),
     ("Water stress across Spain", "西班牙各省水资源压力"),
     ("19 of 50 provinces, home to two-thirds of the population, are under high stress.",
      "50 个省中 19 个处于高压力，涵盖约三分之二人口。")),
    ("sites", "gis", "tiles/sites.webp", "",
     ("Site screening, Hampshire, UK", "选址筛选，英国汉普郡"),
     ("Quiet sites with good access", "安静又交通便利的选址"),
     ("213 km² of quiet land within 5 km of a motorway, matching the original ArcGIS output.",
      "距高速 5 km 内的安静土地共 213 km²，与原 ArcGIS 结果一致。")),
    ("chlorophyll", "optical", "tiles/chlorophyll.webp", "",
     ("Vegetation health", "植被健康"),
     ("Which index tracks chlorophyll", "哪个植被指数最能反映叶绿素"),
     ("The red-edge MTCI explains about 75% of chlorophyll variation; NDVI about 20%.",
      "红边指数 MTCI 能解释约 75% 的叶绿素变化，NDVI 只有约 20%。")),
    ("lidar", "lidar", "tiles/lidar.webp", "",
     ("LiDAR, New Forest, UK. Synthetic demo", "LiDAR，英国 New Forest，合成数据演示"),
     ("LiDAR forest inventory workflow", "LiDAR 森林清查流程"),
     ("Canopy height, stand metrics and a ranked list of compartments for field checks.",
      "林冠高度、林分指标，以及最需要实地核查的林区排序。")),
]
# Order on the wall: keep the two false-colour (red) scenes apart.
ORDER = ["valencia", "earthquakes", "wildfire", "chlorophyll", "glasgow", "spain", "sites", "lidar"]
CASES.sort(key=lambda c: ORDER.index(c[0]))

tiles = "\n".join(f"""        <a class="case t-{slug}{' fit' if fit else ''}" href="case/{slug}.html" data-tags="{tags}">
          <div class="ph"><img src="assets/{img}" alt="" loading="lazy"></div>
          <div class="cap">
            <p class="label" data-zh="{lab[1]}">{lab[0]}</p>
            <h3 data-zh="{title[1]}">{title[0]}</h3>
            <p class="key" data-zh="{key[1]}">{key[0]}</p>
          </div>
        </a>""" for slug, tags, img, fit, lab, title, key in CASES)

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Xiaoqiao Liu, Earth observation</title>
<meta name="description" content="Remote sensing and GIS analyst: flood mapping, InSAR ground deformation, forest carbon, urban heat and GIS automation from satellite radar, LiDAR and optical data.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap">
<link rel="stylesheet" href="assets/v2.css?v=3">
<link rel="icon" href="assets/icon.svg" type="image/svg+xml">
<meta property="og:title" content="Xiaoqiao Liu, Earth observation">
<meta property="og:description" content="Flood mapping, InSAR ground deformation, forest carbon and urban heat from satellite radar, LiDAR and optical data.">
<meta property="og:image" content="https://7ao6688-hash.github.io/assets/og.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
</head>
<body>
"""

BODY = f"""<header class="top">
  <div class="wrap">
    <a class="brand" href="#top">Xiaoqiao Liu <span>Earth observation</span></a>
    <nav class="links" aria-label="Sections">
      <a href="#work" data-zh="案例">Work</a>
      <a href="#lab" data-zh="互动工具">Lab</a>
      <a href="#services" data-zh="服务">Services</a>
      <a href="#about" data-zh="关于我">About</a>
      <a href="#contact" data-zh="联系">Contact</a>
      <button class="lang" id="lang" type="button" aria-label="Switch language">中文</button>
    </nav>
  </div>
</header>

<main id="top">
  <div class="hero wrap">
    <div class="hero-text">
      <h1 data-zh="把卫星数据变成可以据此决策的答案。">Satellite data turned into answers you can act on.</h1>
      <div class="hero-side">
        <p class="label" data-zh="遥感与 GIS 分析师，常驻英国">Remote sensing and GIS analyst, based in the UK</p>
        <p class="lede" data-zh="我用雷达、LiDAR 和光学卫星影像绘制洪水范围、测量地表形变、估算森林碳储量、定位城市热点。每个结果都附带地图、可直接使用的数据和一份简明报告。">I map floods, measure ground movement, estimate forest carbon and find urban hot spots from radar, LiDAR and optical satellite imagery. Every result comes with maps, ready-to-use data and a short plain-language report.</p>
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
      <figcaption>
        <p id="compare-cap" data-zh="瓦伦西亚，2024 年 10 月。Landsat 8 真彩色：洪水后一天，阿尔武费拉潟湖周边的农田被褐色洪水覆盖。左右拖动影像对比洪水前后。">Valencia, October 2024. Landsat 8 true colour: the day after the flood, brown water covers the fields around the Albufera lagoon. Drag across the image to compare.</p>
        <div class="seg" role="group" aria-label="Sensor">
          <button type="button" id="mode-optical" aria-pressed="true" data-zh="光学">Optical</button>
          <button type="button" id="mode-radar" aria-pressed="false" data-zh="雷达">Radar</button>
        </div>
      </figcaption>
    </figure>
  </div>

  <section id="work">
    <div class="wrap">
      <div class="sec-head">
        <h2 data-zh="作品">Work</h2>
        <p data-zh="八个研究项目，每个都有公开的代码、测试和结果。点任意一张图看完整案例。">Eight research projects, each with public code, tests and results. Open any image for the full case study.</p>
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

# The hero caption is the scene description; keep the sensor wording in the script's captions in step with it.
script = script.replace('en: "Sentinel-1 radar (VV). Calm water reflects the signal away, so flooded rice fields turn black. Drag to compare before and after."',
                        'en: "Valencia, October 2024. Sentinel-1 radar: calm water reflects the signal away, so flooded rice fields turn black. Drag across the image to compare."')
script = script.replace('en: "Landsat 8 true colour. The day after the flood, brown floodwater covers the fields around the Albufera lagoon. Drag to compare."',
                        'en: "Valencia, October 2024. Landsat 8 true colour: the day after the flood, brown water covers the fields around the Albufera lagoon. Drag across the image to compare."')

script = script.replace('let mode = "radar";', 'let mode = "optical";')
# Service examples point at tiles on the classic page; here they open the case studies directly.
BODY = BODY.replace('href="#case-valencia"', 'href="case/valencia.html"').replace('href="#case-insar"', 'href="case/earthquakes.html"')            .replace('href="#case-wildfire"', 'href="case/wildfire.html"').replace('href="#case-glasgow"', 'href="case/glasgow.html"')            .replace('href="#case-sites"', 'href="case/sites.html"')
assert "#case-" not in BODY
html = HEAD + BODY + script + "</body>\n</html>\n"   # script includes the lab.js tag
(here / "v2.html").write_text(html, encoding="utf-8")
print(f"v2.html written ({len(html) // 1024} KB)")
