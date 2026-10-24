"""Generate the case-study pages in case/ from one template. Run after editing CASES."""
from pathlib import Path

HERE = Path(__file__).parent
TERMS = {
    "SAR": "Synthetic aperture radar. The satellite sends its own microwave pulses, so it images through cloud, day or night.",
    "VV": "The radar sends and receives vertically polarised waves. VV is the channel most sensitive to open water.",
    "dB": "Decibels: a log scale for radar brightness. Every 10 dB is a factor of ten in reflected energy.",
    "MNDWI": "Modified Normalised Difference Water Index: (green − shortwave infrared) ÷ (green + shortwave infrared). Water scores above zero.",
    "Otsu": "Otsu's method picks the threshold that best separates two groups in a histogram, here water and land, without a human choosing it.",
    "InSAR": "Interferometric SAR: comparing the phase of two radar images taken days apart reveals ground movement of centimetres or less.",
    "LOS": "Line of sight: radar only measures movement towards or away from the satellite, not up, down or sideways separately.",
    "coherence": "How similar the two radar images are, from 0 to 1. Low coherence (vegetation, water, big changes) means the measurement isn't reliable.",
    "unwrapping": "Radar phase repeats every half wavelength (2.8 cm). Unwrapping counts the repeats to rebuild one continuous displacement map.",
    "dNBR": "Difference in Normalised Burn Ratio before and after a fire. The bigger the drop, the more severely the vegetation burned.",
    "AGB": "Above-ground biomass: the dry weight of trunks, branches and leaves, in tonnes per hectare.",
    "LST": "Land-surface temperature: how hot the ground and roofs are, measured from thermal infrared. It isn't the air temperature people feel.",
    "NDVI": "Normalised Difference Vegetation Index: (near infrared − red) ÷ (near infrared + red). Higher values mean more, healthier vegetation.",
    "bootstrap": "Resampling the data many times to see how much a result could vary by chance, which gives a confidence interval.",
    "WTA": "Withdrawal-to-availability ratio: yearly water demand divided by the water generated locally. Above 0.4 counts as high stress.",
    "buffer": "A zone of fixed width drawn around a feature, for example all land within 5 km of a motorway.",
    "red edge": "The steep rise in leaf reflectance between red and near-infrared light (about 690–750 nm). Its position shifts with chlorophyll content.",
    "LiDAR": "Light detection and ranging: an aircraft fires laser pulses and times their return, mapping the ground and tree tops in 3D.",
    "CHM": "Canopy height model: the height of the vegetation above the ground, from surface height (DSM) minus ground height (DTM).",
}


def term(word, label=None):
    return f'<span class="term" tabindex="0">{label or word}<span class="def" role="tooltip">{TERMS[word]}</span></span>'


T = term
CASES = [
    {
        "slug": "valencia", "repo": "valencia-flood-2024", "kicker": "Flood mapping · Valencia, Spain · October 2024",
        "title": "Mapping the Valencia DANA flood from space",
        "lede": "On 29 October 2024 a storm dropped more than a year's rain in hours on the towns south of València. Satellite images from before and after show where the water spread, how long it stayed, and which areas were hit hardest.",
        "stats": [("67 km²", "standing water the day after (Landsat)"), ("42 km²", "still flooded on 1 Nov (radar)"),
                  ("14 km²", "left on 6 Nov as it drained"), ("57%", "of the first map confirmed by radar")],
        "hero": ("valencia-radar.webp", "Radar before (20 Oct) and after (1 Nov), and how the radar flood map compares with the Landsat map from 30 Oct."),
        "sections": [
            ("The question", f"<p>Emergency teams and insurers need to know <b>where the water went and for how long</b>, quickly and over a wide area. Ground surveys are slow and dangerous straight after a flood, and storm cloud often blocks ordinary satellite photos.</p>"),
            ("What I did", f"""<ol class="steps">
<li><b>Compared optical images from before and after.</b> Landsat 8 photographed the area on 28 September and again on 30 October, one day after the flood. A water index ({T("MNDWI")}) shows which pixels turned to water.</li>
<li><b>Let the data choose the cut-off.</b> Instead of picking a threshold by eye, {T("Otsu")}'s method found it from the image itself. I then reran the map with the threshold moved up and down to show how much the answer depends on it.</li>
<li><b>Added radar, which sees through cloud.</b> Sentinel-1 {T("SAR")} images from 20 October and 1 November show water as dark areas. A pixel counted as flooded only if it was dark after the flood, not before, and darker by at least 3 {T("dB")}.</li>
<li><b>Tracked the water draining.</b> A second radar pair (25 October and 6 November) shows how much water was left a week later.</li>
<li><b>Counted exposed buildings.</b> I overlaid 79,000 OpenStreetMap building outlines on the flood maps.</li></ol>"""),
            ("What the maps show", f"""<figure class="fig"><img src="../assets/valencia-optical.webp" alt="Landsat true colour before and after, and new standing water" loading="lazy"></figure>
<figcaption>Landsat 8: before (28 Sep), the day after (30 Oct), and the new standing water in blue.</figcaption>
<p>Most of the floodwater sat on the rice paddies and fields around the Albufera lagoon. The two satellites, three days apart, agree on the large bodies of water: radar confirms 57% of the area Landsat mapped, and finds another 3.5 km² that Landsat missed under cloud.</p>
<div class="pair"><figure class="fig"><img src="../assets/valencia-timeline.webp" alt="Bar chart of flooded area on 30 Oct, 1 Nov and 6 Nov" loading="lazy"></figure>
<figure class="fig"><img src="../assets/valencia-towns.webp" alt="Radar brightness change in flooded and comparison towns" loading="lazy"></figure></div>
<p>The worst-hit towns, such as Paiporta and Catarroja, had already drained by the time any satellite passed over, so they don't show up as open water. On radar, though, their buildings became 0.8 to 1.4 dB brighter, while unflooded parts of València changed by only 0.25 to 0.55 dB. Mud, debris and wet walls explain the difference.</p>"""),
            ("How sure can we be?", """<ul class="limits">
<li><b>The building count is a minimum.</b> Only 191 buildings sat in open water on 30 October. Many more were damaged by water that had already drained.</li>
<li><b>The threshold matters.</b> Moving the Landsat threshold by ±0.15 gives 51 to 99 km². That range is reported alongside the main figure.</li>
<li><b>One snapshot per satellite.</b> Flooding that came and went between overpasses can't be seen.</li>
<li><b>Not yet checked against official maps</b> such as the Copernicus Emergency Management Service delineation for this event.</li></ul>"""),
            ("What a client gets", """<ul><li>Flood extent layers (GeoTIFF and GeoPackage) for each date</li><li>A list of exposed buildings and roads</li>
<li>Map sheets and a short report with the uncertainty range, ready for emergency, insurance or planning teams</li><li>The code, so the same analysis can be rerun for the next event</li></ul>"""),
        ],
        "glance": [("Data", ["Landsat 8 Level-2, 30 m", "Sentinel-1 RTC (VV), 10 m", "OpenStreetMap buildings"]),
                   ("Methods", ["MNDWI change detection", "Radar backscatter change", "Otsu thresholds", "Building exposure"]),
                   ("Tools", ["Python, rasterio, GeoPandas", "Microsoft Planetary Computer"])],
        "tech": [("Optical pair", "LC08 198/033, 28 Sep and 30 Oct 2024; QA_PIXEL cloud mask; 91% clear on both dates"),
                 ("Optical rule", "MNDWI after > 0.05 (Otsu) and MNDWI before ≤ 0"),
                 ("Radar pair", "Sentinel-1A orbit 110 descending, 20 Oct and 1 Nov 2024; RTC γ⁰ averaged to 30 m; 3 × 3 speckle filter"),
                 ("Radar rule", "VV after < −12.3 dB (Otsu), VV before ≥ −12.3 dB, change ≤ −3 dB"),
                 ("Follow-up", "Orbit 8, 25 Oct → 6 Nov 2024; 83% of the area observed"),
                 ("Study area", "20 × 25 km, 0.52–0.30° W, 39.28–39.50° N")],
    },
    {
        "slug": "earthquakes", "repo": "insar-deformation-monitoring", "kicker": "Ground deformation · Türkiye and Morocco · 2023",
        "title": "Measuring how far the ground moved in two earthquakes",
        "lede": "Radar satellites can measure ground movement of a few centimetres over thousands of square kilometres. I used them to map the 2023 earthquakes in Türkiye and Morocco, and turned the results into figures that show exactly where the ground shifted most.",
        "stats": [("≈ 74 cm", "change across 10 km near Kahramanmaraş"), ("≈ 15 cm", "uplift towards the satellite in Morocco"),
                  ("2", "earthquakes, two radar geometries"), ("Exact", "match with my original SNAP statistics")],
        "hero": ("turkiye-los.webp", "Ground movement towards (red) and away from (blue) the satellite after the February 2023 Kahramanmaraş earthquakes."),
        "sections": [
            ("The question", f"<p>After a large earthquake, engineers and planners need to know <b>where the ground moved and by how much</b>: it guides damage surveys, rebuilding and hazard maps. GPS stations measure precisely but only at a few points. {T('InSAR')} measures everywhere the satellite can see.</p>"),
            ("What I did", f"""<ol class="steps">
<li><b>Paired radar images from before and after</b> each earthquake: Sentinel-1, 29 January and 10 February 2023 for Türkiye, and 3 and 15 September 2023 for Morocco.</li>
<li><b>Built the interferogram</b> in ESA SNAP: aligned the images, removed the effect of terrain with a digital elevation model, and filtered noise.</li>
<li><b>Unwrapped the fringes</b> with SNAPHU ({T("unwrapping")}) and converted them to centimetres of movement along the {T("LOS", "line of sight")}.</li>
<li><b>Removed unreliable pixels</b> where {T("coherence")} was below 0.3 (Morocco), and summarised the scene with robust statistics.</li>
<li><b>Drew transects</b>, strips across the area, to show how movement changes with distance, with {T("bootstrap")} confidence intervals.</li></ol>"""),
            ("What the maps show", """<div class="pair"><figure class="fig"><img src="../assets/turkiye-profile.webp" alt="Displacement profile across Kahramanmaraş" loading="lazy"></figure>
<figure class="fig"><img src="../assets/morocco-los.webp" alt="Displacement map of the 2023 Al Haouz earthquake" loading="lazy"></figure></div>
<figcaption>Left: a transect through Kahramanmaraş. Right: the Al Haouz earthquake in Morocco.</figcaption>
<p><b>Türkiye.</b> Along a north-west to south-east line through Kahramanmaraş, the ground's movement changes by about 74 cm over just 10 km, 17 to 27 km south-east of the city. That's where the main rupture crossed. Statistics for the city district match the SNAP output from my MSc dissertation exactly.</p>
<p><b>Morocco.</b> An area just south of the epicentre moved up to about 15 cm towards the satellite, while the surrounding mountains barely moved.</p>"""),
            ("How sure can we be?", """<ul class="limits">
<li><b>One viewing direction.</b> Radar only measures movement along its line of sight, so up-down and sideways motion can't be separated from one image pair.</li>
<li><b>Relative values.</b> The numbers are relative to a reference point chosen by the unwrapping software. Differences across the map are what matter.</li>
<li><b>No atmospheric correction or GPS check.</b> Water vapour can add a few centimetres of error, especially in mountains.</li>
<li><b>Processing seams.</b> Straight-edged steps in the map come from how the data is stitched, not from tectonics.</li></ul>"""),
            ("What a client gets", """<ul><li>Displacement maps (GeoTIFF) and profiles across sites of interest</li><li>A table of movement statistics per area</li>
<li>A plain-language note on what the numbers can and can't support</li><li>For monitoring: the same chain rerun on each new Sentinel-1 pass</li></ul>"""),
        ],
        "glance": [("Data", ["Sentinel-1 IW SLC (C-band)", "SRTM 1-arcsec DEM"]),
                   ("Methods", ["Differential InSAR", "Phase unwrapping", "Coherence masking", "Transect statistics"]),
                   ("Tools", ["ESA SNAP, SNAPHU", "Python, NumPy, matplotlib"])],
        "tech": [("Türkiye pair", "S1A orbit 21 descending, 29 Jan → 10 Feb 2023; TOPS chain with ESD; SNAPHU v2.0.4"),
                 ("Türkiye grid", "8 × 8 block median (≈ 93 m); P1–P99 −36 to +94 cm (relative)"),
                 ("Morocco pair", "S1A orbit 45 ascending, 3 → 15 Sep 2023; sub-swath IW1; coherence ≥ 0.3 (13% masked)"),
                 ("Transects", "10 km swath perpendicular to the regional fault strike; 2 km (Türkiye) and 1 km (Morocco) bins"),
                 ("Context", "Türkiye: MSc dissertation, University of Southampton, 2025")],
    },
    {
        "slug": "wildfire", "repo": "wildfire-carbon-loss", "kicker": "Forest carbon · California, USA · 2020",
        "title": "How much carbon did a wildfire release?",
        "lede": "The 2020 Red Salmon Complex fire burned through conifer forest in northern California. Comparing satellite images from before and after, I mapped how badly each area burned and estimated how much carbon the forest lost, along with how uncertain that estimate is.",
        "stats": [("6.8 Mt", "carbon lost from trees (estimate)"), ("71,600 ha", "burned at some severity"),
                  ("10% → 58%", "high-severity area → share of carbon loss"), ("−17% to +46%", "range from the sensitivity test")],
        "hero": ("wildfire-severity.webp", "Burn severity from Sentinel-2: unburned (grey) to high severity (dark red)."),
        "sections": [
            ("The question", "<p>Forest owners, carbon-credit projects and climate reporting need to know <b>how much carbon a fire released</b>. The answer depends on how severely each patch burned and how much wood was there to begin with.</p>"),
            ("What I did", f"""<ol class="steps">
<li><b>Compared Sentinel-2 images</b> from July 2020 (before) and June 2021 (after), at 10 m resolution.</li>
<li><b>Mapped burn severity</b> with the {T("dNBR")}, using standard thresholds for unburned, low, moderate and high severity.</li>
<li><b>Estimated the wood before the fire</b> ({T("AGB")}) from a simple vegetation model, and how much of it each severity class lost.</li>
<li><b>Converted biomass to carbon</b> (48% of dry wood is carbon) and added it up.</li>
<li><b>Stress-tested every assumption</b> by moving each one up and down and rerunning the whole estimate.</li></ol>"""),
            ("What the results show", """<div class="pair"><figure class="fig"><img src="../assets/wildfire-carbon.webp" alt="Map of carbon loss per hectare" loading="lazy"></figure>
<figure class="fig"><img src="../assets/wildfire-share.webp" alt="Share of area and of carbon loss by severity class" loading="lazy"></figure></div>
<p>High-severity burning covered only about 10% of the area but caused <b>58%</b> of the carbon loss. In total the forest lost an estimated 6.8 million tonnes of carbon, about 17% of what it held before.</p>
<figure class="fig"><img src="../assets/wildfire-sensitivity.webp" alt="Sensitivity of the total to each assumption" loading="lazy"></figure>
<p>The sensitivity test shows which assumption matters most: the burn-severity thresholds. Lowering them slightly raises the total by 46%. A client therefore needs a <b>range, not one number</b>, and field plots would narrow it the most.</p>"""),
            ("How sure can we be?", """<ul class="limits">
<li><b>The biomass model is a simple assumption</b>, not calibrated with field measurements. It can be swapped for a published biomass map.</li>
<li><b>Seasons differ.</b> The images are from July and June of different years, so some "low severity" pixels outside the fire are probably just seasonal change.</li>
<li><b>Only living trees above ground are counted.</b> Soil, litter and later tree deaths are left out.</li>
<li>My original coursework reported 4.5 Mt using a different burn layer. The difference is explained in the repository.</li></ul>"""),
            ("What a client gets", """<ul><li>Burn-severity and carbon-loss maps (GeoTIFF)</li><li>Tables by severity class and by area of interest</li>
<li>A sensitivity table showing the plausible range</li><li>Advice on where field plots would reduce uncertainty most</li></ul>"""),
        ],
        "glance": [("Data", ["Sentinel-2, 10 m", "Before: 26 Jul 2020", "After: 1 Jun 2021"]),
                   ("Methods", ["dNBR burn severity", "Biomass and carbon accounting", "One-at-a-time sensitivity"]),
                   ("Tools", ["Python, NumPy, matplotlib"])],
        "tech": [("Index", "NBR = (B8 − B12)/(B8 + B12); dNBR = NBR before − NBR after"),
                 ("Classes", "unburned < 0.10 ≤ low < 0.27 ≤ moderate < 0.44 ≤ high"),
                 ("Biomass", "AGB (t/ha) = 150 × NBR before + 200; retention 100 / 60 / 30 / 0% by class"),
                 ("Carbon", "carbon = AGB loss × 0.48, summed over 0.01 ha pixels"),
                 ("Scene", "53 × 54 km, 285,902 ha, UTM zone 10N")],
    },
    {
        "slug": "glasgow", "repo": "urban-heat-intervention-explorer", "kicker": "Urban heat · Glasgow, UK · June 2019",
        "title": "Finding where greening would cool Glasgow most",
        "lede": "Cities heat up unevenly. Using a single Landsat image from a sunny June morning, I mapped Glasgow's surface temperature, measured how much cooler greener places are, and pinpointed the hot, bare neighbourhoods where planting would help most.",
        "stats": [("4.6 °C", "hotter: built-up land vs grassland"), ("0.9 °C", "cooler for each +0.1 NDVI"),
                  ("25.5 km²", "hot, bare built-up land to prioritise"), ("203 km²", "of the city analysed at 30 m")],
        "hero": ("glasgow-priority.webp", "Hot built-up land with little vegetation, ranked by how much greening could help."),
        "sections": [
            ("The question", f"<p>Councils planning street trees, green roofs and parks need to know <b>where extra greenery would cool the city most</b>. Heat affects health and comfort, and budgets are limited.</p>"),
            ("What I did", f"""<ol class="steps">
<li><b>Measured surface temperature</b> ({T("LST")}) from Landsat 8's thermal band, correcting for how different surfaces emit heat.</li>
<li><b>Mapped vegetation and land cover</b>: {T("NDVI")} from the red and near-infrared bands, and a classification into built-up, water, forest and grassland.</li>
<li><b>Measured the cooling effect of greenery</b> with a regression of temperature on NDVI from 200 random pixels, with a {T("bootstrap")} confidence interval.</li>
<li><b>Ranked priority areas:</b> built-up pixels that are both hot (well above the city average) and low in vegetation.</li>
<li><b>Estimated what greening would buy</b> for small, medium and large increases in NDVI.</li></ol>"""),
            ("What the maps show", """<div class="pair"><figure class="fig"><img src="../assets/glasgow-lst.webp" alt="Glasgow land-surface temperature map" loading="lazy"></figure>
<figure class="fig"><img src="../assets/glasgow-scatter.webp" alt="Scatter plot of temperature against NDVI" loading="lazy"></figure></div>
<p>Built-up land averaged 25.9 °C at the surface on 28 June 2019, against 21.3 °C for grassland. Greener pixels are clearly cooler: about 0.9 °C for every 0.1 increase in NDVI (95% interval 0.7 to 1.0 °C).</p>
<p class="callout">Raising NDVI by 0.10 across the 25.5 km² of priority land, for example with street trees and green roofs, would cool its surface by roughly <b>0.9 °C (0.7 to 1.0 °C)</b>. Try other values in the interactive tool on the home page.</p>"""),
            ("How sure can we be?", """<ul class="limits">
<li><b>Surface, not air.</b> Satellites measure how hot roofs and roads are, not the air temperature people feel.</li>
<li><b>One sunny morning.</b> A single image captures one moment, not a whole summer.</li>
<li><b>Association, not cause.</b> The cooling figures assume the city-wide relationship holds locally. They're for screening, not a promise for any one street.</li>
<li><b>Small water bodies are under-mapped</b> at 30 m resolution.</li></ul>"""),
            ("What a client gets", """<ul><li>Temperature and vegetation maps for the whole city</li><li>A ranked map of priority areas for greening</li>
<li>Cooling scenarios with uncertainty ranges</li><li>An interactive dashboard to explore options with stakeholders</li></ul>"""),
        ],
        "glance": [("Data", ["Landsat 8 OLI/TIRS, 28 Jun 2019", "Glasgow city boundary"]),
                   ("Methods", ["Land-surface temperature retrieval", "Supervised classification", "Regression with bootstrap", "Priority screening"]),
                   ("Tools", ["ENVI, ArcGIS Pro", "Python, NumPy"])],
        "tech": [("LST", "TIRS band 10: radiance → brightness temperature → NDVI-based emissivity → Sobrino correction"),
                 ("Land cover", "Maximum-likelihood classification: built-up 121 km², forest 59 km², grassland 21 km², water 1 km²"),
                 ("Regression", "LST = −8.74 × NDVI + 29.5 °C; R² = 0.46; n = 200; bootstrap 95% CI −10.1 to −7.1"),
                 ("Priority", "built-up, ≥ 0.35 SD above the city mean LST, NDVI < 0.35"),
                 ("Scenarios", "+0.05 → 0.44 °C · +0.10 → 0.87 °C · +0.15 → 1.31 °C")],
    },
    {
        "slug": "spain", "repo": "spain-water-stress", "kicker": "Water resources · Spain",
        "title": "Which Spanish provinces need more water than they generate?",
        "lede": "Spain is one of Europe's most water-stressed countries, but the pressure is very uneven. Using only free global datasets, I compared how much water each province needs for homes and irrigated farms with how much water its own land produces.",
        "stats": [("24%", "of local runoff used, Spain as a whole"), ("19 of 50", "provinces under high stress"),
                  ("≈ ⅔", "of the population lives in them"), ("5.5×", "Alicante's demand vs its own runoff")],
        "hero": ("spain-stress.webp", "Demand divided by locally generated runoff, by province. Darker means more stressed."),
        "sections": [
            ("The question", "<p>Water managers, farmers and investors want to know <b>where demand already outstrips the water a region produces</b>, and what drives it. Answering that consistently across a whole country needs the same data and the same rules everywhere.</p>"),
            ("What I did", f"""<ol class="steps">
<li><b>Estimated supply</b> from TerraClimate runoff (1991–2020 average, about 4 km), converted to cubic metres with each cell's true area.</li>
<li><b>Estimated household demand</b> from WorldPop 2020 population counts at 0.2 m³ per person per day.</li>
<li><b>Estimated irrigation demand</b> from the FAO map of irrigated land at 4,000 m³ per hectare per year.</li>
<li><b>Put everything on one 1 km grid without losing totals.</b> People and hectares were summed or split by area, never stretched or interpolated.</li>
<li><b>Calculated the stress ratio</b> ({T("WTA")}) for each province and tested how it changes when each assumption moves.</li></ol>"""),
            ("What the results show", """<figure class="fig"><img src="../assets/spain-inputs.webp" alt="Maps of runoff, population and irrigated area in Spain" loading="lazy"></figure>
<figcaption>The three inputs: water generated (runoff), people and irrigated land.</figcaption>
<p>Spain as a whole needs about a quarter of the water its land generates, which is already above the "medium-high stress" line. The pattern is very uneven. The south-east (Alicante, Murcia, Valencia) needs four to six times the water it produces, almost all for irrigation. Madrid and Barcelona are stressed because millions of people live on a small area. The Atlantic north has plenty.</p>
<figure class="fig"><img src="../assets/spain-ranking.webp" alt="Provinces ranked by water stress" loading="lazy"></figure>"""),
            ("How sure can we be?", """<ul class="limits">
<li><b>Only local water is counted.</b> Rivers flowing in from upstream, transfers between basins, groundwater and desalination are left out, so south-eastern and downstream provinces look more stressed than their real supply position.</li>
<li><b>The irrigation rate matters most.</b> Between 3,000 and 6,000 m³ per hectare, the national ratio moves from 0.19 to 0.34, but the south-east is highly stressed in every scenario.</li>
<li><b>Annual averages hide droughts</b>, which is when shortages actually happen.</li></ul>"""),
            ("What a client gets", """<ul><li>Stress maps and a province table for any country or region</li><li>Scenario runs for different water-use assumptions</li>
<li>Gridded supply and demand layers to combine with your own data</li><li>A short report on which areas are robustly stressed and which depend on assumptions</li></ul>"""),
        ],
        "glance": [("Data", ["TerraClimate runoff, 1991–2020", "WorldPop 2020 population", "FAO GMIA irrigated area", "Eurostat NUTS 3 provinces"]),
                   ("Methods", ["Area-conserving gridding", "Withdrawal-to-availability ratio", "Scenario testing"]),
                   ("Tools", ["Python, rasterio, GeoPandas"])],
        "tech": [("Grid", "1/120° (≈ 1 km); runoff depth × spherical cell area; population block-summed; irrigated ha split by area"),
                 ("Coefficients", "Domestic 0.2 m³/person/day; irrigation 4,000 m³/ha/yr (tested 3,000–6,000)"),
                 ("Classes", "Low < 0.1 ≤ moderate < 0.2 ≤ medium-high < 0.4 ≤ high"),
                 ("Extent", "Mainland and Balearic provinces (Canaries, Ceuta and Melilla excluded)"),
                 ("Coursework", "Corrects the original: flow accumulation had been used as runoff, and population counts were treated as densities")],
    },
    {
        "slug": "sites", "repo": "quiet-zone-finder", "kicker": "Site screening · Hampshire, UK",
        "title": "Finding quiet land with good motorway access",
        "lede": "A client wants places close to a motorway for easy access, but away from the loudest traffic noise, inside Hampshire's two national parks. I built a small tool that answers this from open government data, and that anyone can rerun by editing a short settings file.",
        "stats": [("92.7 km²", "New Forest, within 5 km"), ("120.7 km²", "South Downs, within 5 km"),
                  ("≤ 0.01%", "difference from the ArcGIS original"), ("0", "commercial licences needed")],
        "hero": ("hampshire-sites.webp", "Dark green: quiet land within 5 km of a motorway. Light green: within 10 km."),
        "sections": [
            ("The question", "<p>Developers, planners and relocation advisers often ask the same kind of question: <b>which land is close enough to key infrastructure but outside a constraint zone?</b> Here the constraint is road noise of 75 decibels or more, the loudest band in the government's noise model.</p>"),
            ("What I did", f"""<ol class="steps">
<li><b>Selected the motorways</b> from Ordnance Survey's open road network.</li>
<li><b>Drew a {T("buffer")}</b> of 5 km and 10 km around them, each merged into one zone.</li>
<li><b>Removed the noisiest land:</b> every part of each park inside DEFRA's ≥ 75 dB road-noise zone.</li>
<li><b>Overlapped</b> the remaining quiet land with each buffer and measured the area.</li>
<li><b>Checked the answer</b> against my original ArcGIS version of the same analysis.</li></ol>"""),
            ("What the results show", """<p>Within 5 km of a motorway and below 75 dB, there are 92.7 km² in the New Forest (16% of the park) and 120.7 km² in the South Downs (7%). Within 10 km, that rises to 277 km² and 351 km². The open-source version agrees with ArcGIS to within 0.01%. The tiny gap comes from how each program draws the curved ends of buffers.</p>
<p class="callout">Everything a client might want to change sits in one short settings file: the parks, distances, road types and noise bands. No programming is needed, and the tool explains mistakes in plain language. For example, if a road type is misspelt, it lists the ones it found.</p>"""),
            ("How sure can we be?", """<ul class="limits">
<li><b>Noise is modelled, not measured</b>, at 4 m above ground. Land with no noise data counts as quiet, which is how the government data are meant to be read.</li>
<li><b>Only two criteria are used.</b> Real site selection would add land ownership, protected habitats, flood risk and planning rules.</li></ul>"""),
            ("What a client gets", """<ul><li>Suitable-land layers (GeoPackage) and an area table</li><li>An overview map</li>
<li>A reusable tool and settings file for new areas and criteria</li><li>Migration of existing ArcGIS/arcpy workflows to open-source Python, with checked results</li></ul>"""),
        ],
        "glance": [("Data", ["DEFRA road noise (LAeq,16h)", "Natural England national parks", "OS Open Roads"]),
                   ("Methods", ["Buffer and overlay analysis", "Constraint mapping", "Validation against ArcGIS"]),
                   ("Tools", ["Python, GeoPandas, Shapely", "Originally ArcGIS Pro (arcpy)"])],
        "tech": [("Steps", "select road class → dissolved buffer per distance → erase excluded noise classes → intersect → area"),
                 ("Validation", "New Forest 5 km: 92.707 (ArcGIS) vs 92.719 km²; South Downs 10 km: 350.625 vs 350.636 km²"),
                 ("Licences", "All inputs under the Open Government Licence v3.0; packaged example data included"),
                 ("Context", "MSc GIS Programming coursework (University of Southampton, 2025), rewritten without arcpy")],
    },
    {
        "slug": "chlorophyll", "repo": "leaf-chlorophyll-indices", "kicker": "Vegetation health · lab and satellite",
        "title": "Which satellite index best tracks plant health?",
        "lede": "Chlorophyll is the pigment that shows how healthy and productive plants are, and dozens of satellite indices claim to measure it. I tested five common ones on 160 lab-measured leaves from eight species, and on field plots seen by Sentinel-2.",
        "stats": [("0.75", "MTCI, average R² within a species"), ("0.76", "MTCI, R² for canopy chlorophyll"),
                  ("≤ 0.21", "NDVI and PSSRa in the lab"), ("160", "leaves from 8 species")],
        "hero": ("chlorophyll-r2.webp", "How well each index explains chlorophyll, in the lab and from the satellite."),
        "sections": [
            ("The question", "<p>Farm advisers, foresters and ecologists use satellite indices to monitor crop vigour and forest health. <b>Choosing the wrong index can hide real problems</b>, because some indices stop responding once plants are moderately green.</p>"),
            ("What I did", f"""<ol class="steps">
<li><b>Measured leaf reflectance</b> from 350 to 1050 nm on 160 leaves, and their chlorophyll content in the lab.</li>
<li><b>Simulated what Sentinel-2 would see</b> by resampling each spectrum to the satellite's bands, including the {T("red edge")} bands.</li>
<li><b>Computed five indices</b>: NDVI, GNDVI, PSSRa, MTCI and IRECI.</li>
<li><b>Tested each index three ways</b>: within each species, pooled across species, and on a species the model had never seen.</li>
<li><b>Repeated the test with real Sentinel-2 images</b> over field plots in the New Forest, for both leaf and canopy chlorophyll.</li></ol>"""),
            ("What the results show", """<figure class="fig"><img src="../assets/chlorophyll-species.webp" alt="Heatmap of R² by species and index" loading="lazy"></figure>
<p>The two indices built on the red-edge bands do best. MTCI explains about three quarters of the chlorophyll variation within a species. IRECI holds up best on a new species, which matters when a model has to work on crops it wasn't trained on. NDVI, the most widely used index, explains almost nothing for several species because it saturates on green leaves.</p>
<figure class="fig"><img src="../assets/chlorophyll-canopy.webp" alt="Sentinel-2 index against canopy chlorophyll" loading="lazy"></figure>
<p>From the satellite, every index tracks <b>canopy</b> chlorophyll (leaf chlorophyll × leaf area) better than leaf chlorophyll alone, because a pixel sees the whole canopy.</p>"""),
            ("How sure can we be?", """<ul class="limits">
<li><b>Single leaves under lab light</b> are cleaner than real 20 m pixels, which mix leaves, branches, soil and shadow.</li>
<li><b>One region and one season</b> (New Forest, April to October 2016) for the satellite part, so the models need recalibrating elsewhere.</li>
<li>The original lab data are course data and aren't redistributed. Results and code are public.</li></ul>"""),
            ("What a client gets", """<ul><li>A recommendation of which index to use for a crop, forest or habitat</li><li>Calibrated index-to-chlorophyll models with error estimates</li>
<li>Seasonal vigour maps from Sentinel-2</li><li>Guidance on how many field samples are needed</li></ul>"""),
        ],
        "glance": [("Data", ["Lab leaf spectra, 350–1050 nm", "Lab chlorophyll measurements", "Sentinel-2 L2A field plots"]),
                   ("Methods", ["Band resampling", "Vegetation indices", "Leave-one-out and leave-one-species-out tests"]),
                   ("Tools", ["Python, pandas, NumPy"])],
        "tech": [("Indices", "MTCI (B6−B5)/(B5−B4) · IRECI (B7−B4)/(B5/B6) · GNDVI · NDVI · PSSRa, with B7 (783 nm) as NIR"),
                 ("Lab results", "Within-species R²: MTCI 0.75, IRECI 0.63, GNDVI 0.60, NDVI 0.20, PSSRa 0.14"),
                 ("Transfer test", "Leave-one-species-out RMSE: IRECI 37.4, MTCI 40.3, NDVI 57.0 µg/cm²"),
                 ("Satellite", "R² for CCC: MTCI 0.76, GNDVI 0.58, NDVI 0.52, IRECI 0.50, PSSRa 0.34"),
                 ("Coursework", "Explains the two inconsistent R² sets in the original report: one within-species, one pooled")],
    },
    {
        "slug": "lidar", "repo": "new-forest-lidar-inventory", "kicker": "LiDAR forest inventory · New Forest, UK",
        "title": "Turning LiDAR into a forest inventory",
        "lede": "Airborne laser scanning measures the height of every tree from above. This project turns LiDAR elevation models into canopy height, stand statistics and a ranked list of the forest areas that most need checking on the ground.",
        "stats": [("3", "height classes: 2–10, 10–15, ≥ 15 m"), ("P95", "robust top-of-canopy height"),
                  ("15", "forest compartments in the original study"), ("Demo", "published with synthetic data")],
        "hero": ("lidar-dashboard.svg", "Inventory dashboard produced by the workflow (synthetic demonstration scene)."),
        "sections": [
            ("The question", f"<p>Forest managers need to know <b>how tall and how dense the trees are, compartment by compartment</b>, to plan thinning, protect habitats and estimate timber or carbon. Measuring every stand on foot is slow, while {T('LiDAR')} covers a whole forest in one flight.</p>"),
            ("What I did", f"""<ol class="steps">
<li><b>Separated ground from vegetation</b> in the laser returns and built a bare-earth model (DTM) and a surface model (DSM).</li>
<li><b>Calculated canopy height</b> ({T("CHM")}) as surface minus ground, with negative values set to zero.</li>
<li><b>Summarised each forest compartment</b>: canopy cover, the share of trees in each height class, and the 95th-percentile height, which ignores stray tall pixels.</li>
<li><b>Tested how stable the results are</b> if the elevation models are off by a few tens of centimetres, or if the height thresholds change.</li>
<li><b>Ranked compartments for field checks</b> with a transparent score, so foresters know where to look first.</li></ol>"""),
            ("What it produces", """<p>In my MSc coursework I applied this to 15 compartments of the New Forest, combining LiDAR with airborne multispectral imagery to classify the canopy. The public version rebuilds the workflow as tested, reusable code. Because the original survey data are licensed, it ships with a <b>synthetic scene</b> with the same structure, so anyone can run it and see the outputs.</p>
<p class="callout">The ranking is a list of where to send field teams first. It doesn't decide where to harvest. In a protected landscape like the New Forest, that decision also depends on habitats, access and permissions.</p>"""),
            ("How sure can we be?", """<ul class="limits">
<li><b>The public results are a demonstration</b>, not field measurements.</li>
<li><b>Vertical errors in the elevation models</b> shift every height. The workflow reports how the rankings change when they do.</li>
<li><b>Height isn't species.</b> Multispectral or field data are needed to tell conifers from broadleaves.</li></ul>"""),
            ("What a client gets", """<ul><li>Canopy height and cover maps</li><li>A compartment table with height classes and P95 height</li>
<li>A prioritised list for field validation</li><li>A data guide for preparing your own LiDAR (LAS/LAZ or GeoTIFF) in PDAL, QGIS or ArcGIS</li></ul>"""),
        ],
        "glance": [("Data", ["Airborne LiDAR (DSM, DTM)", "Forest mask and compartments", "CASI multispectral (coursework)"]),
                   ("Methods", ["Canopy height model", "Zonal statistics", "Sensitivity to vertical bias", "Priority scoring"]),
                   ("Tools", ["Python, NumPy", "ArcGIS (coursework)"])],
        "tech": [("CHM", "max(DSM − DTM, 0) on a common grid and vertical datum"),
                 ("Metrics", "Canopy cover, share in 2–10 / 10–15 / ≥ 15 m classes, P95 height per compartment"),
                 ("Sensitivity", "Vertical bias and threshold scenarios; rank stability reported"),
                 ("Coursework", "Ground points from first/last-return differences, IDW DTM, TIN-to-raster DSM, 15 compartments")],
    },
]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Xiaoqiao Liu</title>
<meta name="description" content="{lede_attr}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@500;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="../assets/case.css">
</head>
<body>
<header class="top"><div class="wrap"><a class="brand" href="../index.html">Xiaoqiao Liu <span>· Earth observation</span></a>
<nav><a href="../index.html#work">Case studies</a><a href="../index.html#lab">Lab</a><a href="../index.html#contact">Contact</a></nav></div></header>
"""


def page(c, others):
    stats = "".join(f"<div><b>{v}</b><span>{k}</span></div>" for v, k in c["stats"])
    sections = "\n".join(f'<section><h2>{h}</h2>\n{body}\n</section>' for h, body in c["sections"])
    glance = "".join(f"<div><h3>{h}</h3><ul>{''.join(f'<li>{i}</li>' for i in items)}</ul></div>" for h, items in c["glance"])
    tech = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in c["tech"])
    nxt = others[(others.index(c) + 1) % len(others)]
    img, cap = c["hero"]
    return HEAD.format(title=c["title"], lede_attr=c["lede"].replace('"', "&quot;")) + f"""<main class="wrap">
<div class="case-head">
<a class="back" href="../index.html#work">← All case studies</a>
<p class="label">{c["kicker"]}</p>
<h1>{c["title"]}</h1>
<p class="lede">{c["lede"]}</p>
<div class="stats">{stats}</div>
</div>
<figure class="hero-fig"><div class="fig"><img src="../assets/{img}" alt="{cap}"></div><figcaption>{cap}</figcaption></figure>
<div class="cols">
<article class="prose">
{sections}
</article>
<aside class="glance">{glance}
<a class="btn" href="https://github.com/7ao6688-hash/{c["repo"]}" target="_blank" rel="noopener">Code and data on GitHub ↗</a>
<a class="btn" href="../index.html#contact" style="background:var(--accent)">Discuss a similar project</a>
</aside>
</div>
<details class="tech"><summary>Technical details</summary><div class="table-wrap"><table>{tech}</table></div></details>
<div class="next"><div><p class="label">Next case study</p><h2><a href="{nxt["slug"]}.html">{nxt["title"]} →</a></h2></div>
<a href="../index.html#work">All case studies</a></div>
</main>
<footer><div class="wrap">© 2026 Xiaoqiao Liu · Satellite data: Copernicus Sentinel, USGS Landsat · Case-study code is MIT-licensed</div></footer>
</body>
</html>
"""


if __name__ == "__main__":
    out = HERE / "case"
    out.mkdir(exist_ok=True)
    for c in CASES:
        (out / f"{c['slug']}.html").write_text(page(c, CASES), encoding="utf-8")
        print("wrote", f"case/{c['slug']}.html")
