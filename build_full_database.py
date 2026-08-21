"""
Script to generate 150+ comprehensive plant leaf disease and solution entries
into disease_info.json for PlantVision AI.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Define the comprehensive 150 disease knowledge store
diseases = {
    # ------------------ SOLANACEOUS CROPS ------------------
    "Tomato_Early_Blight": {
        "disease_name": "Tomato Early Blight",
        "crop": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "crop_group": "Vegetables",
        "category": "Fungal",
        "pathogen": "Alternaria solani",
        "severity_level": "Moderate",
        "severity_score": 65,
        "cause": "Alternaria solani fungal spores overwinter in solanaceous crop residue and soil, germinating rapidly in warm (24-29°C) and humid weather with frequent rainfall or heavy morning dew.",
        "symptoms": [
            "Concentric dark brown to black target-board rings on older lower leaves.",
            "Pronounced yellow chlorotic halo surrounding necrotic spots.",
            "Premature defoliation starting from the bottom of the canopy upwards.",
            "Dark, sunken, leathery lesions on stems and fruit calyxes."
        ],
        "solution": {
            "immediate_action": "Prune and destroy all infected lower foliage immediately using sanitized shears. Avoid overhead sprinkler irrigation.",
            "organic": "Spray bio-fungicide containing Bacillus subtilis or copper octanoate; apply potassium bicarbonate home spray weekly.",
            "chemical": "Apply protectant fungicides (chlorothalonil, mancozeb) or systemic strobilurins (azoxystrobin, pyraclostrobin) rotating every 7-10 days."
        },
        "prevention": [
            "Practice 3-year crop rotation avoiding other Solanaceae (potato, pepper, eggplant).",
            "Apply 5-8 cm of clean organic straw mulch to prevent soil spore splash.",
            "Ensure wide plant spacing (60-90 cm) for maximum sun drying and airflow.",
            "Irrigate at soil level early in the morning using drip lines."
        ],
        "caution": "Do not compost infected foliage as fungal spores survive domestic compost temperatures. Wear gloves when handling diseased tissue.",
        "recommended_questions": [
            "What organic spray recipe works best for Tomato Early Blight?",
            "Can I safely consume unblemished tomatoes from an affected plant?",
            "How often should I alternate copper fungicide with bio-fungicides?"
        ]
    },
    "Tomato_Late_Blight": {
        "disease_name": "Tomato Late Blight",
        "crop": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "crop_group": "Vegetables",
        "category": "Oomycete / Water Mold",
        "pathogen": "Phytophthora infestans",
        "severity_level": "Critical",
        "severity_score": 98,
        "cause": "Phytophthora infestans oomycete reproduces explosively in cool (15-22°C), overcast, and persistently wet conditions with relative humidity exceeding 90%.",
        "symptoms": [
            "Large, irregular water-soaked pale-to-dark olive lesions expanding across leaves.",
            "Delicate white fuzzy fungal-like growth on the undersides of leaves during damp mornings.",
            "Stems turn dark brown or black, leading to rapid vine collapse.",
            "Greasy, firm, dark brown mottled rot on developing green and ripe tomato fruits."
        ],
        "solution": {
            "immediate_action": "Quarantine the plot immediately. Carefully rogue out and bag severely diseased plants in sealed plastic bags to prevent airborne sporangia dispersal.",
            "organic": "Apply copper hydroxide or Bordeaux mixture proactively before rainfall. Organic eradicants are ineffective once infection is widespread.",
            "chemical": "Apply specialized systemic oomyceticides (mandipropamid, cyazofamid, dimethomorph, or mefenoxam) tank-mixed with contact protectants (mancozeb)."
        },
        "prevention": [
            "Plant certified late-blight resistant cultivars (e.g., Defiant, Mountain Merit, Iron Lady).",
            "Destroy all volunteer potato and tomato plants before planting season.",
            "Maintain wide spacing and prune suckers to optimize canopy air movement.",
            "Sign up for regional university agricultural extension blight warning alerts."
        ],
        "caution": "Late blight is extraordinarily contagious and wind-dispersed across dozens of miles. Immediate quarantine action is mandatory.",
        "recommended_questions": [
            "Will neighboring potato or eggplant beds also catch Tomato Late Blight?",
            "Can I save seeds from a tomato plant that survived Late Blight?",
            "What fungicide class works fastest to halt active Late Blight?"
        ]
    },
    "Tomato_Leaf_Mold": {
        "disease_name": "Tomato Leaf Mold",
        "crop": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "crop_group": "Vegetables",
        "category": "Fungal",
        "pathogen": "Passalora fulva (Cladosporium fulvum)",
        "severity_level": "Moderate",
        "severity_score": 60,
        "cause": "Passalora fulva is a persistent greenhouse and high-tunnel pathogen thriving under high humidity (>85%) and moderate temperatures (20-25°C).",
        "symptoms": [
            "Pale greenish-yellow chlorotic spots with indistinct diffuse margins on upper leaf surfaces.",
            "Dense olive-green to velvety brown moldy sporulation on matching lower leaf surfaces.",
            "Infected leaves curl, wither, turn yellow-brown, and drop prematurely.",
            "Blossoms and calyxes may abort in high disease pressure environments."
        ],
        "solution": {
            "immediate_action": "Increase high-tunnel ventilation immediately and lower relative humidity below 80% with circulation fans.",
            "organic": "Spray bio-fungicides with Trichoderma harzianum or potassium bicarbonate solution; sanitize greenhouse walls and benches.",
            "chemical": "Spray protectant fungicides (chlorothalonil, difenoconazole, fluopyram) following label rates."
        },
        "prevention": [
            "Keep greenhouse relative humidity strictly below 80% using exhaust fans and dehumidification.",
            "Avoid overhead sprinkler irrigation; always use drip lines.",
            "Select leaf-mold resistant tomato hybrids (carrying Cf resistance genes).",
            "Disinfect greenhouse frames and trellising between crop cycles."
        ],
        "caution": "Wear an N95 respiratory mask when working in enclosed greenhouses with heavy spore concentrations to prevent respiratory irritation.",
        "recommended_questions": [
            "How do I manage greenhouse ventilation to completely prevent Leaf Mold?",
            "Are baking soda sprays effective against Tomato Leaf Mold?"
        ]
    },
    "Tomato_Bacterial_Spot": {
        "disease_name": "Tomato Bacterial Spot",
        "crop": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "crop_group": "Vegetables",
        "category": "Bacterial",
        "pathogen": "Xanthomonas perforans / euvesicatoria",
        "severity_level": "High",
        "severity_score": 78,
        "cause": "Seed-borne and splash-dispersed bacteria that enter through leaf stomata and microscopic wounds during warm (25-30°C) rainy periods.",
        "symptoms": [
            "Small (1-3 mm) dark brown to black water-soaked angular spots on foliage.",
            "Thin translucent yellow halos surrounding lesions.",
            "Defoliation resulting in severe sunscald on unprotected fruit.",
            "Raised, scabby, rough black specks with whitish margins on green tomato fruit."
        ],
        "solution": {
            "immediate_action": "Halt overhead irrigation immediately; do not prune or cultivate while foliage is wet.",
            "organic": "Apply preventative fixed copper bactericides mixed with Bacillus amyloliquefaciens; use hot-water treated seeds.",
            "chemical": "Tank-mix copper hydroxide with mancozeb to overcome copper tolerance, or apply registered bacteriophages."
        },
        "prevention": [
            "Always use certified disease-free or hot-water treated seeds (50°C for 25 min).",
            "Maintain a 2-3 year rotation away from solanaceous crops.",
            "Disinfect seed trays, seedling benches, and pruning shears with quaternary ammonium.",
            "Use drip irrigation under black plastic mulch."
        ],
        "caution": "Bacteria spread instantaneously on wet hands and tools. Never harvest or prune wet tomato vines.",
        "recommended_questions": [
            "Why is copper mixed with mancozeb for bacterial spot?",
            "How do I sterilize my tomato pruning tools?"
        ]
    },
    "Tomato_Septoria_Leaf_Spot": {
        "disease_name": "Tomato Septoria Leaf Spot",
        "crop": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "crop_group": "Vegetables",
        "category": "Fungal",
        "pathogen": "Septoria lycopersici",
        "severity_level": "Moderate",
        "severity_score": 68,
        "cause": "Septoria lycopersici overwinters in plant debris and nightshade weeds, releasing spores during warm (20-26°C), wet, rainy weather.",
        "symptoms": [
            "Numerous small circular spots (2-4 mm) with dark brown margins and sunken grayish-white centers.",
            "Tiny black specks (pycnidia fruiting bodies) visible inside mature spots.",
            "Lower leaves turn completely yellow and drop off rapidly.",
            "Fruits remain unaffected directly, but suffer extreme sunscald due to heavy leaf drop."
        ],
        "solution": {
            "immediate_action": "Prune away heavily spotted lower foliage; apply thick mulch to block spore splash.",
            "organic": "Spray copper fungicides or sulfur sprays at 7-day intervals; apply bio-fungicide Bacillus subtilis.",
            "chemical": "Spray chlorothalonil, mancozeb, or azoxystrobin at early symptom onset."
        },
        "prevention": [
            "Mulch beds with straw or plastic to create a physical barrier over soil.",
            "Stake and prune tomato vines for upright growth and maximum sunlight.",
            "Eradicate horsenettle and wild nightshade weeds near tomato patches.",
            "Rotate crops for at least 3 years away from tomatoes."
        ],
        "caution": "Do not till infected tomato residue into the soil at season end without burying it deeply, or remove and burn it.",
        "recommended_questions": [
            "How do I tell the difference between Septoria Leaf Spot and Early Blight?",
            "Does Septoria Leaf Spot infect the tomato fruit itself?"
        ]
    },
    "Tomato_Target_Spot": {
        "disease_name": "Tomato Target Spot",
        "crop": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "crop_group": "Vegetables",
        "category": "Fungal",
        "pathogen": "Corynespora cassiicola",
        "severity_level": "Moderate",
        "severity_score": 66,
        "cause": "Corynespora cassiicola survives on weeds and crop debris, proliferating in warm (20-30°C) and humid sub-tropical conditions.",
        "symptoms": [
            "Small water-soaked pinpoint spots on upper leaf surfaces expanding into brown circular lesions with light brown centers.",
            "Concentric rings resembling a target board with yellow halos.",
            "Premature leaf drop leading to exposed vines.",
            "Sunken, brown, circular lesions on tomato fruit with cracked centers."
        ],
        "solution": {
            "immediate_action": "Prune infected leaves and improve canopy air circulation.",
            "organic": "Apply copper octanoate or neem extract emulsified with potassium silicate.",
            "chemical": "Spray pyraclostrobin, boscalid, fluxapyroxad, or chlorothalonil."
        },
        "prevention": [
            "Increase row spacing and maintain vigorous pruning of lower suckers.",
            "Avoid overhead irrigation.",
            "Practice continuous weed control around garden borders."
        ],
        "caution": "Target spot can rapidly attack fruit directly, making produce unmarketable.",
        "recommended_questions": ["What fungicides are best for Target Spot on greenhouse tomatoes?"]
    },
    "Tomato_Powdery_Mildew": {
        "disease_name": "Tomato Powdery Mildew",
        "crop": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "crop_group": "Vegetables",
        "category": "Fungal",
        "pathogen": "Leveillula taurica / Oidium neolycopersici",
        "severity_level": "Moderate",
        "severity_score": 55,
        "cause": "Airborne fungal spores thriving in warm, dry weather with high relative humidity at night (15-28°C).",
        "symptoms": [
            "White talcum-powder-like patches on upper leaf surfaces.",
            "Yellow chlorotic blotches on corresponding leaf surfaces.",
            "Leaves turn brittle, curl upwards, turn brown, and drop prematurely."
        ],
        "solution": {
            "immediate_action": "Spray affected leaves thoroughly including undersides with sulfur or potassium bicarbonate.",
            "organic": "Apply sulfur dust/spray, potassium bicarbonate (1 tbsp/gal with liquid soap), or neem oil.",
            "chemical": "Spray myclobutanil, triflumizole, or difenoconazole."
        },
        "prevention": [
            "Plant powdery mildew-resistant tomato varieties.",
            "Maintain good air circulation through proper spacing and staking.",
            "Apply preventative sulfur sprays during warm dry spells."
        ],
        "caution": "Do not apply sulfur within 14 days of any oil-based spray (e.g. neem oil) to prevent severe leaf scorch.",
        "recommended_questions": ["How do I safely make a milk spray for powdery mildew?"]
    },
    "Tomato_Yellow_Leaf_Curl_Virus": {
        "disease_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "crop": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "crop_group": "Vegetables",
        "category": "Viral",
        "pathogen": "Tomato Yellow Leaf Curl Begomovirus",
        "severity_level": "Critical",
        "severity_score": 92,
        "cause": "Transmitted exclusively by the sweetpotato whitefly (Bemisia tabaci). The virus replicates systemically in the plant vascular system.",
        "symptoms": [
            "Severe upward leaf curling and cupping (spoon-shaped leaves).",
            "Interveinal yellowing (chlorosis) and reduced leaf size.",
            "Extreme plant stunting with a bushy, erect, bonsai-like appearance.",
            "Blossoms drop before fruit set; virtually zero fruit yield if infected early."
        ],
        "solution": {
            "immediate_action": "Rogue out and destroy infected plants immediately to prevent whiteflies from vectoring virus to neighboring crops.",
            "organic": "Control whitefly vectors using yellow sticky traps, insecticidal soap, pyrethrins, and neem oil.",
            "chemical": "Apply systemic insecticides (imidacloprid, acetamiprid, cyantraniliprole) to control whitefly populations."
        },
        "prevention": [
            "Plant TYLCV-resistant tomato cultivars (e.g., Tycoon, Camaro, Chef's Choice).",
            "Use 50-mesh insect-proof netting in greenhouses and nursery seedling beds.",
            "Use reflective silver/aluminum mulches to repel incoming whiteflies.",
            "Maintain a host-free fallow period between crop cycles."
        ],
        "caution": "There is no chemical cure once a plant is infected with TYLCV. Management relies 100% on vector control and resistant varieties.",
        "recommended_questions": [
            "Can a tomato plant recover from Yellow Leaf Curl Virus?",
            "What is the best organic whitefly trap setup?"
        ]
    },
    "Tomato_Mosaic_Virus": {
        "disease_name": "Tomato Mosaic Virus (ToMV)",
        "crop": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "crop_group": "Vegetables",
        "category": "Viral",
        "pathogen": "Tomato Mosaic Tobamovirus",
        "severity_level": "High",
        "severity_score": 85,
        "cause": "Extremely stable virus transmitted mechanically via contaminated hands, clothing, pruning shears, and seed coats.",
        "symptoms": [
            "Mottling of light and dark green mosaic patterns on foliage.",
            "Shoestring or fern-like leaf distortion and blistering.",
            "Stunted plant growth and reduced fruit size with internal brown ring necrosis."
        ],
        "solution": {
            "immediate_action": "Remove and incinerate infected plants. Wash hands and tools in non-fat milk (10% solution) or detergent.",
            "organic": "No organic cure exists. Practice strict hygiene and seed sanitation.",
            "chemical": "No chemical treatment is effective against plant viruses."
        },
        "prevention": [
            "Plant certified ToMV-resistant cultivars (marked with 'T' or 'ToMV').",
            "Soak seeds in 10% trisodium phosphate (TSP) for 20 minutes before planting.",
            "Wash hands thoroughly with soap before handling tomato plants (tobacco users must be extra cautious)."
        ],
        "caution": "ToMV can survive in dried plant debris and on wooden greenhouse stakes for years. Disinfect all stakes with 10% bleach.",
        "recommended_questions": ["Why does milk help neutralize tobacco and tomato mosaic virus?"]
    },
    "Tomato_Healthy": {
        "disease_name": "Tomato - Healthy Leaf",
        "crop": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "crop_group": "Vegetables",
        "category": "Healthy",
        "pathogen": "None (Healthy)",
        "severity_level": "None",
        "severity_score": 0,
        "cause": "Optimal plant vigor, balanced nutrient uptake, proper hydration, and intact cellular structure.",
        "symptoms": [
            "Uniform vibrant green coloration across leaf blades.",
            "Smooth, intact margins with healthy venation.",
            "No spots, necrotic patches, or insect stippling."
        ],
        "solution": {
            "immediate_action": "Maintain routine cultural care, scouting, and balanced drip irrigation.",
            "organic": "Feed with balanced organic compost tea, seaweed extract, and calcium amendments.",
            "chemical": "No chemical treatment required."
        },
        "prevention": [
            "Continue weekly preventative scouting for hornworms, aphids, and fungal spots.",
            "Maintain regular watering schedule to prevent blossom end rot.",
            "Ensure mulch layer remains intact."
        ],
        "caution": "Keep inspecting underleaf surfaces for early pest colonizers.",
        "recommended_questions": ["What is the ideal N-P-K fertilizer ratio for blooming tomatoes?"]
    },

    # ------------------ POTATO CROPS ------------------
    "Potato_Early_Blight": {
        "disease_name": "Potato Early Blight",
        "crop": "Potato",
        "scientific_name": "Solanum tuberosum",
        "crop_group": "Vegetables",
        "category": "Fungal",
        "pathogen": "Alternaria solani",
        "severity_level": "Moderate",
        "severity_score": 62,
        "cause": "Alternaria solani attacks mature potato foliage under alternating warm (20-30°C) wet and dry conditions.",
        "symptoms": [
            "Dark brown angular spots with target-board concentric rings.",
            "Yellowing surrounding leaf spots leading to foliar desiccation.",
            "Dark, sunken, leathery lesions on potato tubers with raised purple-brown margins."
        ],
        "solution": {
            "immediate_action": "Avoid nutrient stress; ensure steady potassium and nitrogen supply to maintain canopy vigor.",
            "organic": "Apply biological fungicides (Bacillus subtilis) and liquid copper sprays before bloom.",
            "chemical": "Apply protectants (chlorothalonil, mancozeb) or translaminars (pyraclostrobin, boscalid)."
        },
        "prevention": [
            "Plant certified disease-free seed tubers.",
            "Rotate fields on a 3-4 year cycle with non-solanaceous crops (grains, legumes).",
            "Avoid late afternoon or evening overhead irrigation."
        ],
        "caution": "Allow tuber skin to mature before harvest to prevent tuber blight infection in storage.",
        "recommended_questions": ["How do I prevent tuber infection at potato harvest?"]
    },
    "Potato_Late_Blight": {
        "disease_name": "Potato Late Blight",
        "crop": "Potato",
        "scientific_name": "Solanum tuberosum",
        "crop_group": "Vegetables",
        "category": "Oomycete / Water Mold",
        "pathogen": "Phytophthora infestans",
        "severity_level": "Critical",
        "severity_score": 98,
        "cause": "Historical cause of the Irish Potato Famine. Phytophthora infestans causes rapid field collapse in cool (15-20°C), moist weather.",
        "symptoms": [
            "Water-soaked dark lesions spreading rapidly across foliage.",
            "White mildew growth on leaf undersides in humid mornings.",
            "Stems develop dark brown to black rot; tubers exhibit dry granular reddish-brown rot."
        ],
        "solution": {
            "immediate_action": "Desiccate/burn down vine canopy 2-3 weeks before harvest to prevent spores washing into tubers.",
            "organic": "Apply copper fungicides proactively before infection.",
            "chemical": "Apply systemic fungicides (mefenoxam, fluopicolide, cyazofamid) with protectants (mancozeb)."
        },
        "prevention": [
            "Destroy all potato cull piles and volunteer potatoes before spring.",
            "Plant certified disease-free seed potatoes.",
            "Hill soil generously around potato crowns to shield tubers."
        ],
        "caution": "Infected tubers in storage can lead to rapid total bin breakdown from secondary soft rot.",
        "recommended_questions": ["How deep should potato hills be to protect tubers from blight?"]
    },
    "Potato_Blackleg": {
        "disease_name": "Potato Blackleg & Soft Rot",
        "crop": "Potato",
        "scientific_name": "Solanum tuberosum",
        "crop_group": "Vegetables",
        "category": "Bacterial",
        "pathogen": "Pectobacterium atrosepticum / carotovorum",
        "severity_level": "High",
        "severity_score": 82,
        "cause": "Tuber-borne and soil-inhabiting bacteria that thrive in cool, wet soils early in the season, spreading as temperatures rise.",
        "symptoms": [
            "Inky black, slimy decay extending up the stem from the seed piece.",
            "Upper leaves turn pale yellow, roll upward, and wilt suddenly.",
            "Stems become hollow and collapse; tubers produce foul-smelling soft rot."
        ],
        "solution": {
            "immediate_action": "Remove and discard diseased plants and decaying seed pieces from the field.",
            "organic": "Treat seed tubers with bio-control bacteria; ensure well-drained soil.",
            "chemical": "No chemical bactericide cure exists; treat cut seed pieces with mancozeb-streptomycin seed protectant."
        },
        "prevention": [
            "Plant whole certified seed tubers or allow cut seed pieces to suberize (heal) for 3-5 days before planting.",
            "Avoid planting in cold, waterlogged soils below 10°C.",
            "Disinfect seed cutting knives and grading equipment with quaternary ammonium."
        ],
        "caution": "Never wash potatoes in recycled water without continuous sanitizing chlorination.",
        "recommended_questions": ["What is suberization and why does it prevent blackleg in potatoes?"]
    },
    "Potato_Common_Scab": {
        "disease_name": "Potato Common Scab",
        "crop": "Potato",
        "scientific_name": "Solanum tuberosum",
        "crop_group": "Vegetables",
        "category": "Bacterial / Actinomycete",
        "pathogen": "Streptomyces scabies",
        "severity_level": "Moderate",
        "severity_score": 58,
        "cause": "Streptomyces scabies survives indefinitely in neutral-to-alkaline soils (pH > 5.5) and infects developing tubers during dry periods.",
        "symptoms": [
            "Rough, corky, elevated or pitted brownish lesions on potato tuber skin.",
            "Foliage is generally asymptomatic, but tuber cosmetic quality is severely degraded."
        ],
        "solution": {
            "immediate_action": "Maintain soil moisture at 80-85% field capacity during tuber initiation (2-6 weeks after emergence).",
            "organic": "Incorporate green manure crops (rye, clover) and elemental sulfur to acidify soil.",
            "chemical": "Apply seed treatments containing fludioxonil or mancozeb."
        },
        "prevention": [
            "Maintain soil pH between 5.0 and 5.2 in potato fields.",
            "Ensure regular irrigation during the critical 6-week tuber initiation period.",
            "Plant scab-resistant potato varieties (e.g., Superior, Dark Red Norland, Goldrush)."
        ],
        "caution": "Avoid applying fresh uncomposted manure or agricultural lime immediately before planting potatoes.",
        "recommended_questions": ["How does soil pH control potato scab?"]
    },
    "Potato_Healthy": {
        "disease_name": "Potato - Healthy Leaf",
        "crop": "Potato",
        "scientific_name": "Solanum tuberosum",
        "crop_group": "Vegetables",
        "category": "Healthy",
        "pathogen": "None (Healthy)",
        "severity_level": "None",
        "severity_score": 0,
        "cause": "Optimal tuber bulking, balanced nitrogen-potassium ratio, and vigorous foliar canopy.",
        "symptoms": [
            "Smooth, lustrous green compound foliage with intact margins.",
            "Erect stem structure and normal flowering.",
            "Absence of lesions, mottling, or wilting."
        ],
        "solution": {
            "immediate_action": "Maintain uniform hill coverage and steady drip irrigation.",
            "organic": "Apply organic kelp meal and compost.",
            "chemical": "No intervention required."
        },
        "prevention": [
            "Scout weekly for Colorado potato beetles and leafhoppers.",
            "Maintain soil moisture at 2.5 cm water per week."
        ],
        "caution": "Keep monitoring underleaf surfaces for early pest colonizers.",
        "recommended_questions": ["When is the best time to hill potatoes?"]
    },

    # ------------------ PEPPER & EGGPLANT CROPS ------------------
    "Pepper_Bell_Bacterial_Spot": {
        "disease_name": "Pepper Bell Bacterial Spot",
        "crop": "Pepper Bell",
        "scientific_name": "Capsicum annuum",
        "crop_group": "Vegetables",
        "category": "Bacterial",
        "pathogen": "Xanthomonas euvesicatoria",
        "severity_level": "High",
        "severity_score": 79,
        "cause": "Seed-borne and rain-splashed bacteria that penetrate stomata during hot (25-32°C), humid, and stormy weather.",
        "symptoms": [
            "Small (1-3 mm) circular water-soaked spots turning yellow-green with dark brown centers.",
            "Massive foliar leaf drop exposing developing peppers to severe sunscald.",
            "Raised, rough, wart-like brown spots on pepper fruit skin."
        ],
        "solution": {
            "immediate_action": "Avoid working in pepper fields while leaves are wet; use drip irrigation.",
            "organic": "Apply fixed copper bactericides mixed with Bacillus amyloliquefaciens.",
            "chemical": "Tank-mix copper hydroxide with mancozeb, or apply acibenzolar-S-methyl (plant defense activator)."
        },
        "prevention": [
            "Plant resistant pepper hybrids (races 1-10 resistance).",
            "Implement a 2-3 year crop rotation away from solanaceous crops.",
            "Use hot-water treated seeds (50°C for 25 min)."
        ],
        "caution": "Bacterial spot on bell peppers leads to rapid defoliation and severe fruit sunscald.",
        "recommended_questions": ["Which bell pepper varieties are resistant to Bacterial Spot?"]
    },
    "Pepper_Bell_Anthracnose": {
        "disease_name": "Pepper Bell Anthracnose",
        "crop": "Pepper Bell",
        "scientific_name": "Capsicum annuum",
        "crop_group": "Vegetables",
        "category": "Fungal",
        "pathogen": "Colletotrichum acutatum / gloeosporioides",
        "severity_level": "High",
        "severity_score": 77,
        "cause": "Fungal spores spread by rain splash in warm (27°C) wet weather, attacking both green and ripe fruit.",
        "symptoms": [
            "Circular sunken lesions on pepper fruit with concentric rings of salmon-pink to orange spore masses.",
            "Lesions turn black and leathery as tiny black microsclerotia form.",
            "Leaves may exhibit small brown spots with yellow margins."
        ],
        "solution": {
            "immediate_action": "Harvest and discard all infected fruit immediately.",
            "organic": "Apply copper sulfate or bio-fungicide Bacillus subtilis.",
            "chemical": "Spray azoxystrobin, pyraclostrobin, or chlorothalonil starting at first flowering."
        },
        "prevention": [
            "Use certified pathogen-free seed.",
            "Mulch heavily with plastic or straw to stop splash dispersal.",
            "Practice 3-year crop rotation."
        ],
        "caution": "Anthracnose can cause total loss of ripe bell pepper harvests during wet late-summer periods.",
        "recommended_questions": ["What is the best fungicide spray timing for pepper anthracnose?"]
    },
    "Pepper_Bell_Healthy": {
        "disease_name": "Pepper Bell - Healthy Leaf",
        "crop": "Pepper Bell",
        "scientific_name": "Capsicum annuum",
        "crop_group": "Vegetables",
        "category": "Healthy",
        "pathogen": "None (Healthy)",
        "severity_level": "None",
        "severity_score": 0,
        "cause": "Healthy solanaceous vigor with balanced micronutrients and clean foliage.",
        "symptoms": [
            "Glossy, emerald green leaves with intact margins.",
            "Strong crown flowering and sturdy branching.",
            "No curling, chlorosis, or necrotic spots."
        ],
        "solution": {
            "immediate_action": "Maintain balanced drip irrigation and calcium nutrition.",
            "organic": "Feed with organic fish-kelp fertilizer.",
            "chemical": "No treatment required."
        },
        "prevention": [
            "Support plants with stakes or cages to prevent heavy fruit branch breakage."
        ],
        "caution": "Avoid excess nitrogen, which produces lush leaves at the expense of pepper fruiting.",
        "recommended_questions": ["How do I prevent blossom drop in bell peppers?"]
    },
    "Eggplant_Phomopsis_Blight": {
        "disease_name": "Eggplant Phomopsis Blight",
        "crop": "Eggplant",
        "scientific_name": "Solanum melongena",
        "crop_group": "Vegetables",
        "category": "Fungal",
        "pathogen": "Phomopsis vexans",
        "severity_level": "High",
        "severity_score": 80,
        "cause": "Phomopsis vexans overwinters in soil and seed, spreading in warm (28-32°C) rainy weather.",
        "symptoms": [
            "Large, circular brown lesions with gray centers on leaves.",
            "Concentric rings of black pycnidia inside leaf spots.",
            "Pale sunken soft rot lesions on eggplant fruit that shrivel into black mummies."
        ],
        "solution": {
            "immediate_action": "Remove and destroy blighted fruits and lower foliage.",
            "organic": "Apply copper fungicides or bio-fungicide Bacillus amyloliquefaciens.",
            "chemical": "Spray azoxystrobin, mancozeb, or chlorothalonil."
        },
        "prevention": [
            "Use certified disease-free seed.",
            "Rotate crops for at least 3 years away from solanaceous species.",
            "Use drip irrigation under black mulch."
        ],
        "caution": "Infected fruit rot rapidly in transit and storage.",
        "recommended_questions": ["How do I manage Phomopsis blight in eggplant fields?"]
    },

    # ------------------ CEREALS & GRAINS ------------------
    "Rice_Blast": {
        "disease_name": "Rice Blast",
        "crop": "Rice",
        "scientific_name": "Oryza sativa",
        "crop_group": "Cereals & Grains",
        "category": "Fungal",
        "pathogen": "Magnaporthe oryzae (Pyricularia oryzae)",
        "severity_level": "Critical",
        "severity_score": 96,
        "cause": "Magnaporthe oryzae is one of the most destructive cereal pathogens worldwide, thriving in high humidity (>90%) with nighttime temperatures of 17-23°C and excessive nitrogen fertilization.",
        "symptoms": [
            "Diamond-shaped or spindle-shaped lesions with gray/whitish centers and dark reddish-brown borders on leaf blades.",
            "Lesions enlarge, coalesce, and cause total leaf kill (leaf blast).",
            "Neck rot / collar rot causing broken panicles and complete grain emptiness."
        ],
        "solution": {
            "immediate_action": "Drain standing water temporarily; immediately cease nitrogen top-dressing.",
            "organic": "Apply bio-fungicides with Pseudomonas fluorescens or Trichoderma; apply silicon soil amendments.",
            "chemical": "Spray tricyclazole, azoxystrobin, isoprothiolane, or kasugamycin at boot/heading stage."
        },
        "prevention": [
            "Plant blast-resistant rice cultivars (containing Pi resistance genes).",
            "Avoid excessive nitrogen fertilization; balance with potassium and silicon.",
            "Maintain proper water depth management in paddy fields.",
            "Treat seeds with carbendazim or tricyclazole before sowing."
        ],
        "caution": "Neck blast infection at panicle emergence can cause 100% crop loss in susceptible fields.",
        "recommended_questions": [
            "How does silicon fertilization protect rice from blast disease?",
            "What is the best timing for tricyclazole spray against neck blast?"
        ]
    },
    "Rice_Brown_Spot": {
        "disease_name": "Rice Brown Spot",
        "crop": "Rice",
        "scientific_name": "Oryza sativa",
        "crop_group": "Cereals & Grains",
        "category": "Fungal",
        "pathogen": "Bipolaris oryzae (Cochliobolus miyabeanus)",
        "severity_level": "High",
        "severity_score": 75,
        "cause": "Historical cause of the 1943 Great Bengal Famine. Bipolaris oryzae thrives in nutrient-deficient, poorly drained, or drought-stressed soils.",
        "symptoms": [
            "Numerous small, oval or circular dark brown to purplish-brown spots on leaves and glumes.",
            "Mature spots have a distinct light brown or gray center with a yellow halo resembling sesame seeds.",
            "Grain discoloration and unfilled grains."
        ],
        "solution": {
            "immediate_action": "Apply balanced foliar potassium and zinc fertilizer to alleviate crop stress.",
            "organic": "Seed treatment with Trichoderma viride or Pseudomonas fluorescens.",
            "chemical": "Spray mancozeb, propiconazole, or iprodione at tillering and heading."
        },
        "prevention": [
            "Improve soil fertility with balanced NPK, zinc, and organic matter.",
            "Treat seeds with hot water (53-54°C for 10-12 min) or fungicide.",
            "Ensure uniform field leveling and consistent water management."
        ],
        "caution": "Brown spot is strongly associated with poor, nutrient-deficient soils. Soil health correction is paramount.",
        "recommended_questions": ["Why is Rice Brown Spot called a 'poor man's disease'?"]
    },
    "Rice_Sheath_Blight": {
        "disease_name": "Rice Sheath Blight",
        "crop": "Rice",
        "scientific_name": "Oryza sativa",
        "crop_group": "Cereals & Grains",
        "category": "Fungal",
        "pathogen": "Rhizoctonia solani",
        "severity_level": "High",
        "severity_score": 84,
        "cause": "Soil and water-borne sclerotia float on paddy water during warm (28-32°C) and humid weather, attacking dense high-tillering canopies.",
        "symptoms": [
            "Oval or irregular greenish-gray water-soaked spots on leaf sheaths near the waterline.",
            "Lesions expand, turning bleached-gray with dark brown borders.",
            "Blight progresses upward to the flag leaf, causing whole tillers to lodge."
        ],
        "solution": {
            "immediate_action": "Lower paddy water depth to promote air circulation at the base.",
            "organic": "Apply bio-agent Pseudomonas fluorescens or Bacillus subtilis to the irrigation water.",
            "chemical": "Spray validamycin, hexaconazole, thifluzamide, or azoxystrobin at early tillering."
        },
        "prevention": [
            "Avoid overly dense planting populations and excessive nitrogen fertilizer.",
            "Skim floating sclerotia during final paddy land preparation.",
            "Practice crop rotation with non-host crops."
        ],
        "caution": "Thifluzamide and validamycin have strict pre-harvest intervals in commercial rice production.",
        "recommended_questions": ["How do sclerotia survive in paddy soil between seasons?"]
    },
    "Rice_Bacterial_Leaf_Blight": {
        "disease_name": "Rice Bacterial Leaf Blight (BLB)",
        "crop": "Rice",
        "scientific_name": "Oryza sativa",
        "crop_group": "Cereals & Grains",
        "category": "Bacterial",
        "pathogen": "Xanthomonas oryzae pv. oryzae",
        "severity_level": "Critical",
        "severity_score": 90,
        "cause": "Xanthomonas oryzae penetrates hydathodes and wounds during monsoonal rains, typhoon winds, and high temperatures (25-34°C).",
        "symptoms": [
            "Water-soaked translucent stripes starting at leaf tips and wavy margins.",
            "Lesions turn straw-yellow to bleached-white, causing entire leaf blades to dry and roll.",
            "Milky or amber bacterial ooze droplets on young lesions in humid mornings (Kresek wilt phase)."
        ],
        "solution": {
            "immediate_action": "Drain excess field water and withhold nitrogen fertilization immediately.",
            "organic": "Apply fresh cow-dung extract spray or bio-formulations of plant extracts.",
            "chemical": "Spray copper hydroxide mixed with plantomycin or validamycin."
        },
        "prevention": [
            "Plant BLB-resistant rice varieties with Xa resistance genes (e.g. IR64, Improved Samba Mahsuri).",
            "Avoid clipping seedling leaf tips during transplanting.",
            "Ensure field sanitation and destroy wild grass hosts (Leersia hexandra)."
        ],
        "caution": "Bacterial blight spreads rapidly during flooding and severe storms. Field drainage is critical.",
        "recommended_questions": ["What is the Kresek symptom of bacterial leaf blight in rice?"]
    },
    "Rice_Healthy": {
        "disease_name": "Rice - Healthy Leaf",
        "crop": "Rice",
        "scientific_name": "Oryza sativa",
        "crop_group": "Cereals & Grains",
        "category": "Healthy",
        "pathogen": "None (Healthy)",
        "severity_level": "None",
        "severity_score": 0,
        "cause": "Optimal paddy ecology, balanced nutrient management, and healthy tiller architecture.",
        "symptoms": [
            "Erect, bright emerald green linear leaf blades with clean midribs.",
            "Clean leaf sheaths with no waterline lesions.",
            "Vigorous panicle emergence."
        ],
        "solution": {
            "immediate_action": "Maintain optimal flood depth and scheduled top-dressing.",
            "organic": "Apply neem cake and green manure.",
            "chemical": "No intervention required."
        },
        "prevention": [
            "Maintain alternate wetting and drying (AWD) water management."
        ],
        "caution": "Scout for leaf folders and stem borers regularly.",
        "recommended_questions": ["What is Alternate Wetting and Drying (AWD) in rice cultivation?"]
    },

    # ------------------ WHEAT & BARLEY CROPS ------------------
    "Wheat_Stripe_Rust": {
        "disease_name": "Wheat Stripe (Yellow) Rust",
        "crop": "Wheat",
        "scientific_name": "Triticum aestivum",
        "crop_group": "Cereals & Grains",
        "category": "Fungal",
        "pathogen": "Puccinia striiformis f. sp. tritici",
        "severity_level": "Critical",
        "severity_score": 94,
        "cause": "Puccinia striiformis spores travel thousands of miles on jet streams, developing rapidly in cool (9-15°C) and humid spring weather.",
        "symptoms": [
            "Bright yellow-orange powdery pustules (uredinia) arranged in long linear stripes parallel to leaf veins.",
            "Leaves appear stitched with yellow lines, later drying into brown necrotic stripes.",
            "Severe shriveling of wheat grains."
        ],
        "solution": {
            "immediate_action": "Spray systemic triazole fungicide immediately upon first detection of stripe foci.",
            "organic": "Sulfur-based foliar protectants applied before disease onset.",
            "chemical": "Apply propiconazole, tebuconazole, or azoxystrobin + cyproconazole."
        },
        "prevention": [
            "Plant resistant wheat cultivars with Yr resistance genes (Yr18, Yr29).",
            "Monitor regional wheat rust surveillance and spore trap maps.",
            "Eradicate volunteer wheat plants during the green bridge period."
        ],
        "caution": "Stripe rust spreads with explosive speed in cool climates. Early spray timing is vital.",
        "recommended_questions": ["What is the 'green bridge' in cereal rust epidemiology?"]
    },
    "Wheat_Leaf_Rust": {
        "disease_name": "Wheat Leaf (Brown) Rust",
        "crop": "Wheat",
        "scientific_name": "Triticum aestivum",
        "crop_group": "Cereals & Grains",
        "category": "Fungal",
        "pathogen": "Puccinia triticina",
        "severity_level": "High",
        "severity_score": 80,
        "cause": "Puccinia triticina flourishes in moderate temperatures (15-22°C) with dew periods of 6+ hours.",
        "symptoms": [
            "Small, circular to oval, cinnamon-brown powdery pustules scattered randomly across upper leaf surfaces.",
            "Pustules rupture the leaf epidermis, causing moisture loss and premature leaf death."
        ],
        "solution": {
            "immediate_action": "Apply foliar triazole fungicide if rust reaches flag leaf before heading.",
            "organic": "Apply biological protectants (Bacillus-based).",
            "chemical": "Spray tebuconazole, prothioconazole, or pyraclostrobin."
        },
        "prevention": [
            "Plant wheat cultivars with adult plant resistance (APR) genes (Lr34).",
            "Plant early to escape peak late-spring airborne spore loads."
        ],
        "caution": "Protecting the flag leaf is critical, as it contributes up to 75% of grain fill carbohydrates.",
        "recommended_questions": ["Why is the flag leaf the most critical leaf to protect in wheat?"]
    },
    "Wheat_Powdery_Mildew": {
        "disease_name": "Wheat Powdery Mildew",
        "crop": "Wheat",
        "scientific_name": "Triticum aestivum",
        "crop_group": "Cereals & Grains",
        "category": "Fungal",
        "pathogen": "Blumeria graminis f. sp. tritici",
        "severity_level": "Moderate",
        "severity_score": 65,
        "cause": "Blumeria graminis proliferates in dense, heavily fertilized canopies under cool (15-20°C) and humid weather.",
        "symptoms": [
            "White to grayish cottony/fluffy mycelial mats on lower leaves and stems.",
            "Mats turn dull gray-brown with tiny embedded black specks (chasmothecia).",
            "Affected leaves yellow, senesce, and die prematurely."
        ],
        "solution": {
            "immediate_action": "Apply foliar fungicide if mildew ascends into the middle canopy before flag leaf emergence.",
            "organic": "Sulfur dusting or potassium bicarbonate sprays.",
            "chemical": "Spray proquinazid, cyflufenamid, fenpropimorph, or metconazole."
        },
        "prevention": [
            "Select resistant cultivars carrying Pm genes.",
            "Avoid excessive nitrogen fertilization and high seeding rates."
        ],
        "caution": "Do not exceed maximum seasonal application limits of DMI fungicides to avoid resistance.",
        "recommended_questions": ["How does nitrogen rate impact powdery mildew severity in wheat?"]
    },
    "Wheat_Healthy": {
        "disease_name": "Wheat - Healthy Leaf",
        "crop": "Wheat",
        "scientific_name": "Triticum aestivum",
        "crop_group": "Cereals & Grains",
        "category": "Healthy",
        "pathogen": "None (Healthy)",
        "severity_level": "None",
        "severity_score": 0,
        "cause": "Optimal tillering and stem extension vigor with vibrant chlorophyll distribution.",
        "symptoms": [
            "Clean, linear blue-green to dark green leaf blades.",
            "No pustules, streaks, or white mildew coatings.",
            "Strong flag leaf and healthy head emergence."
        ],
        "solution": {
            "immediate_action": "Maintain balanced top-dressing and soil moisture.",
            "organic": "Organic kelp and compost extract.",
            "chemical": "No intervention required."
        },
        "prevention": ["Scout fields weekly from jointing through grain filling."],
        "caution": "Keep monitoring for aphid vectors of Barley Yellow Dwarf Virus.",
        "recommended_questions": ["What are the critical growth stages for wheat yield determination?"]
    },
    "Corn_Common_Rust": {
        "disease_name": "Corn Common Rust",
        "crop": "Corn (Maize)",
        "scientific_name": "Zea mays",
        "crop_group": "Cereals & Grains",
        "category": "Fungal",
        "pathogen": "Puccinia sorghi",
        "severity_level": "Moderate",
        "severity_score": 58,
        "cause": "Puccinia sorghi urediniospores blow in on southern storm fronts during moderate temperatures (16-25°C) and high humidity.",
        "symptoms": [
            "Small, cinnamon-brown to reddish-orange powdery pustules scattered on both upper and lower leaf surfaces.",
            "Pustules rupture the epidermis, releasing powdery spores.",
            "Pustules turn brownish-black late in the season as resting spores (teliospores) form."
        ],
        "solution": {
            "immediate_action": "Assess rust coverage on the ear leaf; apply fungicide if susceptible sweet corn or inbred lines are near tasseling.",
            "organic": "Sulfur-based fungicides or bio-fungicides applied early.",
            "chemical": "Apply triazole or strobilurin fungicides (pyraclostrobin + metconazole, azoxystrobin + propiconazole)."
        },
        "prevention": [
            "Select hybrids with single-gene (Rp) or high general horizontal resistance.",
            "Plant early in the season to evade peak airborne spore flights.",
            "Maintain balanced crop nutrition."
        ],
        "caution": "Follow fungicide label pre-harvest intervals (PHI) closely on sweet corn for fresh market consumption.",
        "recommended_questions": ["At what growth stage does common rust impact corn yield the most?"]
    },
    "Corn_Northern_Leaf_Blight": {
        "disease_name": "Corn Northern Leaf Blight (NCLB)",
        "crop": "Corn (Maize)",
        "scientific_name": "Zea mays",
        "crop_group": "Cereals & Grains",
        "category": "Fungal",
        "pathogen": "Exserohilum turcicum (Setosphaeria turcica)",
        "severity_level": "High",
        "severity_score": 75,
        "cause": "Exserohilum turcicum overwinters in corn residue and spreads rapidly during moderate temperatures (18-27°C) with 6+ hours of leaf wetness.",
        "symptoms": [
            "Long, elliptical, cigar-shaped grayish-green to tan lesions (2.5 to 15 cm long) parallel to leaf veins.",
            "Dark olive-green to black fungal sporulation visible within older lesions during damp periods.",
            "Canopy takes on a scorched, grayish-brown appearance."
        ],
        "solution": {
            "immediate_action": "If lesions are present on leaves below the ear before tasseling, protect upper canopy with fungicide.",
            "organic": "Apply biological protectants (Bacillus-based); bury infected crop residue.",
            "chemical": "Apply foliar fungicides containing strobilurins and triazoles (fluxapyroxad + pyraclostrobin, prothioconazole + trifloxystrobin) around VT/R1 stage."
        },
        "prevention": [
            "Plant resistant corn hybrids carrying Ht resistance genes.",
            "Rotate with non-host crops like soybeans, wheat, or alfalfa for at least one year.",
            "Incorporate or chop crop residue to accelerate decomposition."
        ],
        "caution": "Residue-borne fungal conidia remain viable in minimum-till fields for over 12 months.",
        "recommended_questions": ["How can I differentiate Northern Leaf Blight from Gray Leaf Spot in corn?"]
    },
    "Corn_Gray_Leaf_Spot": {
        "disease_name": "Corn Gray Leaf Spot (GLS)",
        "crop": "Corn (Maize)",
        "scientific_name": "Zea mays",
        "crop_group": "Cereals & Grains",
        "category": "Fungal",
        "pathogen": "Cercospora zeae-maydis",
        "severity_level": "High",
        "severity_score": 82,
        "cause": "Cercospora zeae-maydis survives in surface corn residue, proliferating under warm (25-32°C), humid weather with persistent morning dews.",
        "symptoms": [
            "Small tan spots with yellow halos expanding into distinct rectangular, blocky lesions restricted by parallel leaf veins.",
            "Lesions become opaque, grayish-brown, and may coalesce to blight entire leaves.",
            "Premature stalk lodging and severe loss of grain test weight."
        ],
        "solution": {
            "immediate_action": "Apply dual-mode foliar fungicide at tasseling (VT) to silking (R1) if lesions reach the third leaf below the ear.",
            "organic": "Practice crop rotation and residue management.",
            "chemical": "Spray premix fungicides containing strobilurin + triazole + SDHI (e.g., Miravis Neo, Trivapro, Veltyma)."
        },
        "prevention": [
            "Select corn hybrids with high GLS tolerance ratings.",
            "Rotate with soybeans or non-grass crops for at least 1-2 years.",
            "Use vertical tillage to bury residue in high-risk continuous-corn fields."
        ],
        "caution": "GLS is the #1 foliar yield-limiting disease in no-till continuous corn systems across the Americas.",
        "recommended_questions": ["What is the ROI of spraying fungicide for Gray Leaf Spot on field corn?"]
    },
    "Corn_Healthy": {
        "disease_name": "Corn (Maize) - Healthy Leaf",
        "crop": "Corn (Maize)",
        "scientific_name": "Zea mays",
        "crop_group": "Cereals & Grains",
        "category": "Healthy",
        "pathogen": "None (Healthy)",
        "severity_level": "None",
        "severity_score": 0,
        "cause": "Optimal photosynthetic efficiency, strong root anchorage, and balanced nitrogen supply.",
        "symptoms": [
            "Broad, unblemished emerald green leaves with prominent pale midribs.",
            "Absence of lesions, rust pustules, or insect feeding scars.",
            "Vigorous silk and tassel development."
        ],
        "solution": {
            "immediate_action": "Ensure adequate moisture during silking and pollination.",
            "organic": "Organic compost side-dressing.",
            "chemical": "No intervention required."
        },
        "prevention": [
            "Ensure regular soil fertility testing.",
            "Maintain optimal plant population density."
        ],
        "caution": "Avoid water deficit during silking, which causes poor kernel set.",
        "recommended_questions": ["What are the critical water requirements for corn during silking?"]
    },

    # ------------------ FRUIT TREES, VINEYARDS & BERRIES ------------------
    "Apple_Scab": {
        "disease_name": "Apple Scab",
        "crop": "Apple",
        "scientific_name": "Malus domestica",
        "crop_group": "Fruit Trees & Berries",
        "category": "Fungal",
        "pathogen": "Venturia inaequalis",
        "severity_level": "High",
        "severity_score": 76,
        "cause": "Venturia inaequalis ascospores discharge from overwintered leaves during spring rain events between 10-24°C.",
        "symptoms": [
            "Olive-green to velvety dark brown circular spots on leaf surfaces.",
            "Lesions become raised, corky, and puckered, causing premature leaf drop in midsummer.",
            "Fruit develops scabby, cracked, misshapen black lesions that stunt fruit growth."
        ],
        "solution": {
            "immediate_action": "Apply protectant fungicide before anticipated spring rainfall events when green tissue is emerging.",
            "organic": "Apply sulfur, lime-sulfur, potassium bicarbonate, or liquid copper at green tip through petal fall.",
            "chemical": "Apply protectants (mancozeb, captan) or sterol inhibitors (difenoconazole, myclobutanil) timed with Mills infection periods."
        },
        "prevention": [
            "Plant scab-immune apple cultivars (Liberty, Prima, Enterprise, GoldRush, Freedom).",
            "Rake, shred, or spray fallen autumn leaves with 5% urea to accelerate leaf decay.",
            "Prune trees annually during dormancy to open canopy for rapid wind drying."
        ],
        "caution": "Repeated use of single-site fungicides (e.g. strobilurins) can rapidly induce fungal resistance.",
        "recommended_questions": ["What is the Mills Table for apple scab infection prediction?"]
    },
    "Apple_Black_Rot": {
        "disease_name": "Apple Black Rot (Frogeye Leaf Spot)",
        "crop": "Apple",
        "scientific_name": "Malus domestica",
        "crop_group": "Fruit Trees & Berries",
        "category": "Fungal",
        "pathogen": "Botryosphaeria obtusa",
        "severity_level": "Moderate",
        "severity_score": 68,
        "cause": "Botryosphaeria obtusa overwinters in dead wood, mummified apples, and bark cankers, discharging spores during warm, humid rains.",
        "symptoms": [
            "Frogeye leaf spot: small purple spots expanding into circular lesions with light tan centers and purple margins.",
            "Fruit develops firm brown rot with alternating dark and light concentric bands.",
            "Rotting fruit shrivels into black, wrinkled mummies hanging on branches.",
            "Sunken reddish-brown oval cankers on limbs and trunks."
        ],
        "solution": {
            "immediate_action": "Prune out dead wood and cankers at least 15 cm below visible infection; remove all mummified apples.",
            "organic": "Apply copper or sulfur sprays; burn pruned infected branches.",
            "chemical": "Apply captan, thiophanate-methyl, or strobilurin fungicides from petal fall through cover sprays."
        },
        "prevention": [
            "Prune out dead, damaged, and fire-blight injured wood annually.",
            "Remove wild or abandoned apple and cedar trees near the orchard.",
            "Sterilize pruning tools with 70% alcohol between cuts."
        ],
        "caution": "Mummified fruit left on trees are the primary source of spring inoculum.",
        "recommended_questions": ["How do I distinguish Apple Scab from Frogeye Leaf Spot?"]
    },
    "Apple_Fire_Blight": {
        "disease_name": "Apple & Pear Fire Blight",
        "crop": "Apple",
        "scientific_name": "Malus domestica",
        "crop_group": "Fruit Trees & Berries",
        "category": "Bacterial",
        "pathogen": "Erwinia amylovora",
        "severity_level": "Critical",
        "severity_score": 96,
        "cause": "Erwinia amylovora enters blossom nectaries via pollinators and rain splash during warm (18-28°C) spring bloom.",
        "symptoms": [
            "Blossoms and young shoots suddenly wilt, blacken, and shrivel, forming a characteristic 'shepherd's crook' hook.",
            "Leaves turn dark brown/black and remain attached to dead branches, looking scorched by fire.",
            "Milky to amber bacterial ooze droplets on infected shoots.",
            "Sunken, dark bark cankers with cracked margins on scaffold branches and trunks."
        ],
        "solution": {
            "immediate_action": "Prune infected strikes immediately during dry weather, cutting at least 30-45 cm below visible margin into healthy wood.",
            "organic": "Apply fixed copper bactericides at silver tip/green tip; spray biological antagonists (Bacillus subtilis, Pantoea agglomerans) at bloom.",
            "chemical": "Apply agricultural streptomycin or kasugamycin during bloom when predictive models (Maryblyt, Cougarblight) signal infection risk."
        },
        "prevention": [
            "Plant fire blight-resistant rootstocks (Geneva series) and scions.",
            "Avoid excessive nitrogen fertilization, which produces succulent vulnerable shoots.",
            "Disinfect pruning shears in 70% alcohol or 10% bleach between every cut."
        ],
        "caution": "Fire blight can travel systemically to the rootstock within weeks, killing mature trees. Swift pruning is mandatory.",
        "recommended_questions": ["What is the shepherd's crook symptom in fire blight?"]
    },
    "Apple_Healthy": {
        "disease_name": "Apple - Healthy Leaf",
        "crop": "Apple",
        "scientific_name": "Malus domestica",
        "crop_group": "Fruit Trees & Berries",
        "category": "Healthy",
        "pathogen": "None (Healthy)",
        "severity_level": "None",
        "severity_score": 0,
        "cause": "Vigorous orchard canopy, balanced soil minerals, and active leaf cuticle defense.",
        "symptoms": [
            "Glossy, deep green leaves with crisp serrated margins.",
            "Strong spur extension and healthy fruitlet finish.",
            "Absence of scabs, lesions, or rust spots."
        ],
        "solution": {
            "immediate_action": "Maintain routine IPM scouting and foliar calcium sprays.",
            "organic": "Foliar kelp and fish emulsion.",
            "chemical": "No intervention required."
        },
        "prevention": ["Prune annually during dormancy for maximum sunlight penetration."],
        "caution": "Avoid excessive nitrogen which promotes fire blight susceptibility.",
        "recommended_questions": ["What foliar nutrients improve apple fruit finish?"]
    },
    "Grape_Black_Rot": {
        "disease_name": "Grape Black Rot",
        "crop": "Grape",
        "scientific_name": "Vitis vinifera",
        "crop_group": "Fruit Trees & Berries",
        "category": "Fungal",
        "pathogen": "Guignardia bidwellii (Phyllosticta ampelicida)",
        "severity_level": "High",
        "severity_score": 82,
        "cause": "Guignardia bidwellii overwinters in mummified berries and cane cankers, discharging spores during warm (21-32°C) rain events.",
        "symptoms": [
            "Small, reddish-brown circular spots on leaves that enlarge with dark brown borders.",
            "Tiny black fruiting bodies (pycnidia) arranged in a neat ring pattern inside lesions.",
            "Berries turn pale, soften, rapidly shrivel into hard, black, wrinkled mummies.",
            "Purple-black elongated lesions on new shoots."
        ],
        "solution": {
            "immediate_action": "Remove and discard all mummified fruit clusters hanging from the trellis.",
            "organic": "Apply copper sulfate or lime-sulfur sprays starting at bud break through bloom.",
            "chemical": "Spray myclobutanil, tebuconazole, kresoxim-methyl, or mancozeb from early bloom through 4 weeks post-bloom."
        },
        "prevention": [
            "Canopy management: shoot thinning and leaf pulling around clusters to maximize airflow and sun exposure.",
            "Collect and bury or burn all mummies and pruned canes during dormancy.",
            "Plant less susceptible grape cultivars."
        ],
        "caution": "The period from early bloom until 4 to 5 weeks after fruit set is the critical window for fruit infection.",
        "recommended_questions": ["When is the most critical time to spray grapes for Black Rot?"]
    },
    "Grape_Downy_Mildew": {
        "disease_name": "Grape Downy Mildew",
        "crop": "Grape",
        "scientific_name": "Vitis vinifera",
        "crop_group": "Fruit Trees & Berries",
        "category": "Oomycete / Water Mold",
        "pathogen": "Plasmopara viticola",
        "severity_level": "Critical",
        "severity_score": 92,
        "cause": "Plasmopara viticola overwinters as oospores in fallen leaves, germinating in spring during 10-10-10 conditions (10 cm shoot growth, 10 mm rain, 10°C temperature).",
        "symptoms": [
            "Yellowish, oily, translucent 'oil-spots' on upper leaf surfaces.",
            "Dense, white cottony/downy growth on matching lower leaf surfaces.",
            "Infected shoot tips curl, turn brown, and die; young berries shrivel and turn leathery brown."
        ],
        "solution": {
            "immediate_action": "Apply systemic anti-oomycete fungicide immediately upon oil-spot detection.",
            "organic": "Apply copper hydroxide or Bordeaux mixture proactively before rainfall.",
            "chemical": "Spray mandipropamid, cyazofamid, dimethomorph, or fosetyl-aluminum."
        },
        "prevention": [
            "Keep canopy open with shoot positioning and basal leaf removal.",
            "Ensure vineyard floor drainage to minimize humidity.",
            "Spray protectants ahead of predicted wet infection periods."
        ],
        "caution": "Downy mildew can defoliate entire vineyards in midsummer, halting berry sugar accumulation.",
        "recommended_questions": ["What is the 10-10-10 rule for Grape Downy Mildew?"]
    },
    "Grape_Powdery_Mildew": {
        "disease_name": "Grape Powdery Mildew",
        "crop": "Grape",
        "scientific_name": "Vitis vinifera",
        "crop_group": "Fruit Trees & Berries",
        "category": "Fungal",
        "pathogen": "Erysiphe necator (Uncinula necator)",
        "severity_level": "High",
        "severity_score": 85,
        "cause": "Erysiphe necator thrives in shaded, low-light canopies under warm (20-27°C) dry weather without requiring free water.",
        "symptoms": [
            "White to ash-gray powdery coating on leaves, green shoots, and fruit clusters.",
            "Leaves curl upward and exhibit web-like brown patches.",
            "Infected berries become scarred, stunted, and split open, inviting secondary bunch rots."
        ],
        "solution": {
            "immediate_action": "Spray sulfur or potassium bicarbonate immediately to eradicate active powdery patches.",
            "organic": "Apply micronized wettable sulfur, potassium bicarbonate, or horticultural stylet oil.",
            "chemical": "Spray quinoxyfen, triflumizole, metrafenone, or boscalid rotating FRAC classes."
        },
        "prevention": [
            "Pull basal leaves around fruit clusters to expose them to direct sunlight (UV light suppresses spores).",
            "Maintain an uninterrupted spray schedule from bud break through veraison."
        ],
        "caution": "Do not apply sulfur when temperatures exceed 32°C (90°F) or within 14 days of oil applications to avoid severe berry burn.",
        "recommended_questions": ["How does sunlight exposure control grape powdery mildew?"]
    },
    "Grape_Healthy": {
        "disease_name": "Grape - Healthy Leaf",
        "crop": "Grape",
        "scientific_name": "Vitis vinifera",
        "crop_group": "Fruit Trees & Berries",
        "category": "Healthy",
        "pathogen": "None (Healthy)",
        "severity_level": "None",
        "severity_score": 0,
        "cause": "Optimal vineyard trellis management, balanced vine vigor, and clean palmate foliage.",
        "symptoms": [
            "Broad, vibrant green leaves with clear veins and uniform texture.",
            "Absence of spots, oil-spots, mildew coatings, or berry rot.",
            "Vigorous shoot growth and clean cluster development."
        ],
        "solution": {
            "immediate_action": "Maintain canopy tucking and shoot positioning.",
            "organic": "Seaweed foliar sprays.",
            "chemical": "No intervention required."
        },
        "prevention": ["Maintain regular canopy thinning and IPM scouting."],
        "caution": "Avoid overly dense canopies that create shaded stagnant microclimates.",
        "recommended_questions": ["What is the ideal vine canopy density for sun penetration?"]
    },
    "Citrus_Canker": {
        "disease_name": "Citrus Canker",
        "crop": "Citrus (Orange, Lemon, Lime)",
        "scientific_name": "Citrus spp.",
        "crop_group": "Fruit Trees & Berries",
        "category": "Bacterial",
        "pathogen": "Xanthomonas citri subsp. citri",
        "severity_level": "Critical",
        "severity_score": 92,
        "cause": "Highly contagious bacteria entering stomata and leafminer wounds during warm (20-30°C) windy rains.",
        "symptoms": [
            "Raised, blister-like corky lesions with crater-like sunken centers on leaves, twigs, and fruit.",
            "Prominent, oily yellow halos surrounding the corky lesions.",
            "Premature defoliation, twig dieback, and severe unmarketable fruit drop."
        ],
        "solution": {
            "immediate_action": "Prune out infected twigs during dry weather; sanitize all harvesting equipment.",
            "organic": "Apply preventative copper sprays every 3 weeks during active flush and fruit development.",
            "chemical": "Spray copper hydroxide mixed with mancozeb, or apply bactericides with zinc."
        },
        "prevention": [
            "Install windbreaks (casuarina, bamboo, eucalyptus) around groves to reduce wind-driven rain speed below 18 mph.",
            "Control Asian citrus leafminers whose feeding galleries provide bacterial infection pathways.",
            "Plant canker-tolerant citrus varieties."
        ],
        "caution": "Citrus canker is a quarantine pathogen in major citrus-producing nations. Follow all regulatory guidelines.",
        "recommended_questions": ["How do windbreaks reduce citrus canker spread?"]
    },
    "Citrus_Greening": {
        "disease_name": "Citrus Greening (Huanglongbing / HLB)",
        "crop": "Citrus (Orange, Lemon, Lime)",
        "scientific_name": "Citrus spp.",
        "crop_group": "Fruit Trees & Berries",
        "category": "Bacterial / Phloem-Limited",
        "pathogen": "Candidatus Liberibacter asiaticus",
        "severity_level": "Critical",
        "severity_score": 99,
        "cause": "Devastating unculturable phloem-limited bacterium transmitted by the Asian citrus psyllid (Diaphorina citri).",
        "symptoms": [
            "Asymmetrical, blotchy yellow mottling across leaf veins (mottle does not match on both halves of leaf).",
            "Vein corking, yellow shoot dieback ('yellow dragon').",
            "Lopsided, bitter, small fruit that remains green at the blossom end ('greening').",
            "Root starvation and total tree decline within 3-5 years."
        ],
        "solution": {
            "immediate_action": "Rogue out infected trees in commercial groves to eliminate reservoir; aggressively control psyllid vectors.",
            "organic": "Release beneficial parasitoid wasps (Tamarixia radiata); apply intensive foliar micronutrients (zinc, iron, manganese).",
            "chemical": "Apply systemic and contact insecticides (imidacloprid, thiamethoxam, spinetoram) to suppress psyllids; trunk injection of oxytetracycline where approved."
        },
        "prevention": [
            "Use only certified disease-free nursery stock grown in insect-proof screenhouses.",
            "Area-wide coordinated psyllid control with neighboring orchards.",
            "Inspect young flush regularly for psyllid nymphs and waxy honeydew secretions."
        ],
        "caution": "HLB is incurable once established in the phloem. Aggressive vector suppression is mandatory.",
        "recommended_questions": ["What is asymmetrical blotchy mottle in citrus greening?"]
    },
    "Banana_Black_Sigatoka": {
        "disease_name": "Banana Black Sigatoka",
        "crop": "Banana",
        "scientific_name": "Musa acuminata",
        "crop_group": "Fruit Trees & Berries",
        "category": "Fungal",
        "pathogen": "Pseudocercospora fijiensis (Mycosphaerella fijiensis)",
        "severity_level": "Critical",
        "severity_score": 95,
        "cause": "Pseudocercospora fijiensis thrives in hot, humid, tropical climates (25-30°C) with continuous rainfall, causing 50%+ yield loss.",
        "symptoms": [
            "Tiny reddish-brown specks on leaf undersides expanding into dark rusty-brown streaks parallel to veins.",
            "Streaks turn dark brown to black, coalesce, and cause rapid collapse of entire leaf blades.",
            "Severe reduction in functional leaf count, causing premature bunch ripening."
        ],
        "solution": {
            "immediate_action": "Deleafing: regularly prune off severely necrotic leaf sections to reduce ascospore inoculum.",
            "organic": "Apply mineral oil (Banole) sprays and bio-fungicides; improve plantation drainage.",
            "chemical": "Spray systemic fungicides (triazoles, strobilurins, SDHIs) emulsified with petroleum oil, strictly alternating FRAC codes."
        },
        "prevention": [
            "Plant Black Sigatoka-resistant hybrid bananas (FHIA hybrids).",
            "Maintain optimal plantation density and drainage ditches.",
            "Execute systematic deleafing rounds every 7-14 days."
        ],
        "caution": "Fungus rapidly develops resistance to systemic fungicides; strict resistance management is vital.",
        "recommended_questions": ["Why is deleafing essential in commercial banana management?"]
    },
    "Mango_Anthracnose": {
        "disease_name": "Mango Anthracnose",
        "crop": "Mango",
        "scientific_name": "Mangifera indica",
        "crop_group": "Fruit Trees & Berries",
        "category": "Fungal",
        "pathogen": "Colletotrichum gloeosporioides",
        "severity_level": "High",
        "severity_score": 85,
        "cause": "Colletotrichum gloeosporioides attacks tender flushes, blossoms, and developing fruit during warm, rainy tropical weather.",
        "symptoms": [
            "Small, dark brown angular leaf spots that coalesce into large necrotic blights.",
            "Blossom blight: flowers turn black, dry, and drop, resulting in zero fruit set.",
            "Black, tear-stain streaks and sunken circular rot spots on ripening mango fruits."
        ],
        "solution": {
            "immediate_action": "Prune diseased twigs and dead panicles after harvest; harvest fruit with pedicels attached.",
            "organic": "Apply copper oxychloride or bio-fungicide Bacillus subtilis; hot water dip harvested fruit (52°C for 5 min).",
            "chemical": "Spray azoxystrobin, difenoconazole, or prochloraz during panicle emergence and fruit set."
        },
        "prevention": [
            "Prune tree centers to allow sunlight and rapid air drying.",
            "Post-harvest hot water treatment to eliminate latent fruit infections."
        ],
        "caution": "Latent infections remain invisible on green fruit and erupt as black rot as fruit ripens.",
        "recommended_questions": ["What is hot water treatment for post-harvest mango anthracnose?"]
    },
    "Peach_Leaf_Curl": {
        "disease_name": "Peach Leaf Curl",
        "crop": "Peach & Nectarine",
        "scientific_name": "Prunus persica",
        "crop_group": "Fruit Trees & Berries",
        "category": "Fungal",
        "pathogen": "Taphrina deformans",
        "severity_level": "High",
        "severity_score": 78,
        "cause": "Taphrina deformans spores overwinter on bark and bud scales, infecting emerging leaves during cool (10-20°C), wet spring weather.",
        "symptoms": [
            "Leaves emerge thick, puckered, twisted, and distorted with vibrant reddish, purple, or yellow discoloration.",
            "Infected foliage turns velvety gray with spore production, dries, and drops in early summer.",
            "Twig stunting and fruit drop."
        ],
        "solution": {
            "immediate_action": "Once symptoms appear in spring, sprays are ineffective. Support tree with water and nitrogen to promote secondary flush.",
            "organic": "Apply dormant copper sulfate or lime-sulfur in late autumn after leaf fall and again in late winter before bud swell.",
            "chemical": "Apply chlorothalonil, ziram, or copper hydroxide during dormancy before bud swell."
        },
        "prevention": [
            "Apply a single thorough dormant fungicide spray after 90% leaf drop in autumn or in early spring before bud break.",
            "Plant resistant peach varieties (e.g. Frost, Avalon Pride, Mary Jane)."
        ],
        "caution": "Spraying after bud break or after leaf curl is visible provides ZERO control for the current season.",
        "recommended_questions": ["Why must peach leaf curl sprays be applied strictly during dormancy?"]
    },
    "Strawberry_Leaf_Spot": {
        "disease_name": "Strawberry Leaf Spot (Common Spot)",
        "crop": "Strawberry",
        "scientific_name": "Fragaria × ananassa",
        "crop_group": "Fruit Trees & Berries",
        "category": "Fungal",
        "pathogen": "Mycosphaerella fragariae",
        "severity_level": "Moderate",
        "severity_score": 60,
        "cause": "Mycosphaerella fragariae spreads by rain splash and overhead irrigation during warm (18-24°C) wet weather.",
        "symptoms": [
            "Small, deep purple to red spots expanding to 3-6 mm on upper leaf surfaces.",
            "Spot centers turn tan to bleached-white, giving a distinct 'bird's-eye' appearance.",
            "Black seed disease on ripening strawberry fruits."
        ],
        "solution": {
            "immediate_action": "Prune and discard infected leaves; switch to drip irrigation under straw mulch.",
            "organic": "Apply copper octanoate, potassium bicarbonate, or Bacillus amyloliquefaciens.",
            "chemical": "Spray pyraclostrobin, captan, or cyprodinil + fludioxonil."
        },
        "prevention": [
            "Plant certified disease-free strawberry crowns.",
            "Ensure wide plant spacing on raised beds.",
            "Renovate strawberry beds after harvest by mowing old foliage."
        ],
        "caution": "Avoid overhead watering in the late afternoon.",
        "recommended_questions": ["How does post-harvest renovation control strawberry leaf diseases?"]
    },

    # ------------------ CUCURBITS & VEGETABLES ------------------
    "Cucumber_Downy_Mildew": {
        "disease_name": "Cucumber Downy Mildew",
        "crop": "Cucumber",
        "scientific_name": "Cucumis sativus",
        "crop_group": "Vegetables",
        "category": "Oomycete / Water Mold",
        "pathogen": "Pseudoperonospora cubensis",
        "severity_level": "Critical",
        "severity_score": 95,
        "cause": "Pseudoperonospora cubensis is an obligate biotrophic oomycete that travels hundreds of miles on storm clouds, attacking cucurbits in humid, dew-laden weather.",
        "symptoms": [
            "Bright yellow angular chlorotic spots strictly bounded by leaf veins on upper leaf surfaces.",
            "Purplish-gray to dark brown downy spore growth on lower leaf surfaces.",
            "Spots turn brown, curl up, and cause leaves to look scorched ('wildfire' symptom)."
        ],
        "solution": {
            "immediate_action": "Apply targeted oomycete fungicides immediately upon regional alert notification.",
            "organic": "Apply copper hydroxide or fixed copper proactively.",
            "chemical": "Spray specialized fungicides (cyazofamid, fluopicolide, propamocarb, oxathiapiprolin) tank-mixed with protectant chlorothalonil."
        },
        "prevention": [
            "Plant downy mildew-tolerant cucumber varieties (e.g. DMR 401, Bristol).",
            "Trellis vines to improve airflow and rapid morning sun drying.",
            "Track the Cucurbit Downy Mildew ipmPIPE forecasting system."
        ],
        "caution": "Downy mildew can completely kill a healthy cucumber patch within 5-7 days of infection.",
        "recommended_questions": ["How do I distinguish cucurbit downy mildew from powdery mildew?"]
    },
    "Cucumber_Powdery_Mildew": {
        "disease_name": "Cucumber Powdery Mildew",
        "crop": "Cucumber",
        "scientific_name": "Cucumis sativus",
        "crop_group": "Vegetables",
        "category": "Fungal",
        "pathogen": "Podosphaera xanthii / Golovinomyces cichoracearum",
        "severity_level": "Moderate",
        "severity_score": 65,
        "cause": "Airborne spores proliferating in shaded canopies and high humidity without needing standing water.",
        "symptoms": [
            "White talcum-powder-like fungal patches on both upper and lower leaf surfaces, petioles, and stems.",
            "Leaves turn chlorotic yellow, become dry and brittle, and die prematurely.",
            "Fruits suffer sunscald and premature ripening with poor flavor."
        ],
        "solution": {
            "immediate_action": "Spray potassium bicarbonate or horticultural oil at first sign of white spots.",
            "organic": "Spray potassium bicarbonate (1 tbsp/gal with soap), neem oil, or sulfur.",
            "chemical": "Spray myclobutanil, triflumizole, quinoxyfen, or cyflufenamid."
        },
        "prevention": [
            "Plant powdery mildew-resistant cucumber cultivars.",
            "Trellis plants to maximize light penetration.",
            "Avoid excessive nitrogen fertilization."
        ],
        "caution": "Do not apply sulfur within 2 weeks of oil sprays.",
        "recommended_questions": ["Can potassium bicarbonate cure active powdery mildew?"]
    },
    "Watermelon_Gummy_Stem_Blight": {
        "disease_name": "Watermelon Gummy Stem Blight / Black Rot",
        "crop": "Watermelon",
        "scientific_name": "Citrullus lanatus",
        "crop_group": "Vegetables",
        "category": "Fungal",
        "pathogen": "Stagonosporopsis cucurbitacearum (Didymella bryoniae)",
        "severity_level": "High",
        "severity_score": 85,
        "cause": "Survives in cucurbit crop residue and wild citron, attacking vines during warm (20-25°C), wet conditions.",
        "symptoms": [
            "Large, circular to irregular brown necrotic lesions starting at leaf margins.",
            "Crown stems develop water-soaked cankers that exude a characteristic gummy, reddish-brown amber ooze.",
            "Black fruiting bodies (pycnidia) embedded in dead tissue; vine wilts suddenly."
        ],
        "solution": {
            "immediate_action": "Prune dead vines; avoid wounding stems during cultivation.",
            "organic": "Apply copper hydroxide and bio-fungicides; use drip lines.",
            "chemical": "Spray chlorothalonil, difenoconazole, tebuconazole, or fluxapyroxad + pyraclostrobin."
        },
        "prevention": [
            "Rotate out of cucurbits for at least 2-3 years.",
            "Use certified pathogen-free seed.",
            "Incorporate crop residue immediately after harvest."
        ],
        "caution": "Gummy stem blight attacks fruit directly (black rot), destroying market value.",
        "recommended_questions": ["What causes the amber gummy ooze on watermelon stems?"]
    },
    "Cabbage_Black_Rot": {
        "disease_name": "Cabbage & Brassica Black Rot",
        "crop": "Cabbage (Broccoli, Cauliflower, Kale)",
        "scientific_name": "Brassica oleracea",
        "crop_group": "Vegetables",
        "category": "Bacterial",
        "pathogen": "Xanthomonas campestris pv. campestris",
        "severity_level": "Critical",
        "severity_score": 92,
        "cause": "Seed-borne and rain-splashed vascular bacteria that enter leaf hydathodes during warm (25-30°C) rainy periods.",
        "symptoms": [
            "Characteristic yellow V-shaped lesions starting at leaf margins with the wide base at the edge and apex pointing toward leaf veins.",
            "Leaf veins inside the V-shaped lesion turn conspicuously black.",
            "Cross-section of the stem reveals a distinctive black ring in the vascular bundle.",
            "Extensive head rot and foul secondary bacterial odors."
        ],
        "solution": {
            "immediate_action": "Rogue out infected plants; never work in brassica fields while wet.",
            "organic": "Apply fixed copper bactericides mixed with Bacillus amyloliquefaciens; use hot-water treated seeds.",
            "chemical": "Spray copper hydroxide + mancozeb or acibenzolar-S-methyl (Actigard)."
        },
        "prevention": [
            "Use hot-water treated seed (50°C for 25-30 min).",
            "Practice a minimum 3-year crop rotation avoiding all crucifers (mustard, radish, kale, broccoli).",
            "Eradicate wild cruciferous weeds (shepherd's purse, wild mustard)."
        ],
        "caution": "Black rot is the most destructive brassica disease worldwide. Seed sanitation is non-negotiable.",
        "recommended_questions": ["What is the V-shaped leaf margin symptom in brassicas?"]
    },
    "Onion_Purple_Blotch": {
        "disease_name": "Onion Purple Blotch",
        "crop": "Onion & Garlic",
        "scientific_name": "Allium cepa",
        "crop_group": "Vegetables",
        "category": "Fungal",
        "pathogen": "Alternaria porri",
        "severity_level": "High",
        "severity_score": 75,
        "cause": "Alternaria porri attacks allium foliage during warm (21-30°C) and humid rainy weather with extended leaf wetness.",
        "symptoms": [
            "Small water-soaked lesions that enlarge into sunken, elliptical purplish-brown lesions with yellow margins.",
            "Concentric rings of dark brown fungal sporulation inside purple lesions.",
            "Leaves girdle, collapse, and dry from tips downward, severely stunting bulb size."
        ],
        "solution": {
            "immediate_action": "Avoid overhead irrigation; ensure wide plant spacing.",
            "organic": "Apply copper oxychloride or bio-fungicide Trichoderma viride.",
            "chemical": "Spray mancozeb, chlorothalonil, azoxystrobin, or difenoconazole."
        },
        "prevention": [
            "Rotate with non-allium crops for 3 years.",
            "Plant disease-free sets or transplants.",
            "Ensure excellent field drainage and avoid late-season nitrogen applications."
        ],
        "caution": "Fungus often enters via onion thrips feeding punctures. Control thrips to reduce purple blotch.",
        "recommended_questions": ["How do thrips accelerate onion purple blotch?"]
    },

    # ------------------ CASH CROPS, LEGUMES & PLANTATIONS ------------------
    "Coffee_Leaf_Rust": {
        "disease_name": "Coffee Leaf Rust (La Roya)",
        "crop": "Coffee",
        "scientific_name": "Coffea arabica",
        "crop_group": "Cash Crops",
        "category": "Fungal",
        "pathogen": "Hemileia vastatrix",
        "severity_level": "Critical",
        "severity_score": 98,
        "cause": "Hemileia vastatrix is an obligate biotrophic fungus that caused the collapse of coffee production in 19th-century Ceylon, thriving in temperatures between 21-25°C with free water.",
        "symptoms": [
            "Pale yellow spots (1-3 mm) on upper leaf surfaces expanding into larger chlorotic circles.",
            "Bright orange-yellow powdery pustules (urediniospores) on the corresponding lower leaf surfaces.",
            "Extensive premature defoliation leaving coffee branches bare ('dieback'), causing 30-80% yield collapse."
        ],
        "solution": {
            "immediate_action": "Prune dead wood and apply protectant copper sprays to new vegetative flushes.",
            "organic": "Apply copper oxychloride or Bordeaux mixture (0.5-1.0%) at the start of the rainy season; apply Bacillus subtilis.",
            "chemical": "Spray systemic triazole/strobilurin fungicides (epoxiconazole, cyproconazole, pyraclostrobin) timed with new leaf flushes."
        },
        "prevention": [
            "Plant rust-resistant Arabica cultivars (Castillo, Ruiru 11, Batian, IPR 100, Catimor/Sarchimor hybrids).",
            "Maintain balanced shade tree density (30-40% canopy cover) to avoid excessive humidity.",
            "Maintain optimal soil nutrition with adequate potassium and nitrogen."
        ],
        "caution": "Coffee Leaf Rust is the single most destructive disease in global coffee agriculture. Preventative spray timing is vital.",
        "recommended_questions": [
            "Which coffee varieties are immune or resistant to Coffee Leaf Rust?",
            "How does shade tree canopy management regulate coffee rust?"
        ]
    },
    "Tea_Blister_Blight": {
        "disease_name": "Tea Blister Blight",
        "crop": "Tea",
        "scientific_name": "Camellia sinensis",
        "crop_group": "Cash Crops",
        "category": "Fungal",
        "pathogen": "Exobasidium vexans",
        "severity_level": "Critical",
        "severity_score": 92,
        "cause": "Exobasidium vexans attacks young succulent tea flushes and harvestable buds during monsoon seasons with heavy mist and low sunshine (<4 hours/day).",
        "symptoms": [
            "Translucent, pale yellow circular spots on young tender leaves.",
            "Spots become sunken on the upper leaf surface and bubble up into white, blister-like swellings on the underside.",
            "Blisters rupture, releasing powdery white basidiospores; young stems break and die."
        ],
        "solution": {
            "immediate_action": "Remove blistered shoots during regular 7-day plucking rounds.",
            "organic": "Apply copper oxychloride (0.2%) mixed with nickel chloride.",
            "chemical": "Spray copper hydroxide or systemic morpholine/triazole fungicides (tridemorph, hexaconazole) at 5-7 day intervals during monsoons."
        },
        "prevention": [
            "Prune shade trees before monsoon season to increase UV light penetration.",
            "Maintain regular, hard plucking rounds to remove susceptible young shoots.",
            "Plant blister blight-tolerant tea clones."
        ],
        "caution": "Strictly observe pre-harvest intervals to ensure zero chemical residue in harvested commercial tea leaves.",
        "recommended_questions": ["How do plucking intervals help control tea blister blight?"]
    },
    "Cotton_Bacterial_Blight": {
        "disease_name": "Cotton Bacterial Blight (Angular Leaf Spot / Blackarm)",
        "crop": "Cotton",
        "scientific_name": "Gossypium hirsutum",
        "crop_group": "Cash Crops",
        "category": "Bacterial",
        "pathogen": "Xanthomonas citri pv. malvacearum",
        "severity_level": "High",
        "severity_score": 85,
        "cause": "Seed-borne and debris-borne bacteria entering stomata during warm (30-35°C), stormy, and humid weather.",
        "symptoms": [
            "Small, angular, water-soaked spots on leaves bounded by veinlets.",
            "Spots turn dark reddish-brown to black, forming 'blackarm' lesions on branches and stems.",
            "Boll rot: circular, dark, water-soaked sunken lesions on cotton bolls staining and rotting lint."
        ],
        "solution": {
            "immediate_action": "Avoid overhead irrigation; destroy crop residue after harvest.",
            "organic": "Delint seed with concentrated sulfuric acid; spray copper bactericides.",
            "chemical": "Treat acid-delinted seed with carboxin + thiram; spray copper oxychloride mixed with streptomycin."
        },
        "prevention": [
            "Plant resistant cotton cultivars carrying B resistance genes.",
            "Acid-delint all planting seed to destroy seed-coat bacterial inoculum.",
            "Rotate crops with non-hosts like sorghum or wheat."
        ],
        "caution": "Acid-delinting is dangerous and must be conducted by certified seed treatment facilities.",
        "recommended_questions": ["What is acid delinting of cotton seed?"]
    },
    "Sugarcane_Red_Rot": {
        "disease_name": "Sugarcane Red Rot",
        "crop": "Sugarcane",
        "scientific_name": "Saccharum officinarum",
        "crop_group": "Cash Crops",
        "category": "Fungal",
        "pathogen": "Colletotrichum falcatum (Glomerella tucumanensis)",
        "severity_level": "Critical",
        "severity_score": 96,
        "cause": "Known as the 'Cancer of Sugarcane'. Fungal spores spread via infected setts and waterlogged soil during warm, humid conditions.",
        "symptoms": [
            "Third or fourth leaf from top yellows, withers, and droops.",
            "Red lesions on the leaf midrib with dark centers.",
            "Internal stalk split reveals deep red discoloration interrupted by distinctive white transverse bands and an alcoholic/sour odor."
        ],
        "solution": {
            "immediate_action": "Uproot and burn diseased clumps immediately; do not ratoon infected fields.",
            "organic": "Moist hot-air treatment of seed setts (54°C for 2.5 hours); apply Trichoderma viride to soil.",
            "chemical": "Dip setts in carbendazim (0.1%) or thiophanate-methyl before planting."
        },
        "prevention": [
            "Use only certified red-rot free seed cane setts from healthy seed nurseries.",
            "Practice hot water treatment (52°C for 30 min) or aerated steam treatment of seed setts.",
            "Avoid water stagnation with deep field drainage channels."
        ],
        "caution": "Never take ratoon crops from a red-rot infected field.",
        "recommended_questions": ["What are the characteristic white transverse patches in sugarcane red rot?"]
    },
    "Soybean_Asian_Rust": {
        "disease_name": "Soybean Asian Rust",
        "crop": "Soybean",
        "scientific_name": "Glycine max",
        "crop_group": "Legumes & Oilseeds",
        "category": "Fungal",
        "pathogen": "Phakopsora pachyrhizi",
        "severity_level": "Critical",
        "severity_score": 98,
        "cause": "Phakopsora pachyrhizi is an aggressive obligate biotrophic pathogen capable of causing 80%+ yield loss under warm (15-28°C) humid conditions with 6+ hours of dew.",
        "symptoms": [
            "Tiny, pinpoint chlorotic specks on lower leaves expanding into tan to reddish-brown polygonal lesions.",
            "Volcano-shaped raised pustules (uredinia) on the underside of leaves exuding masses of tan spores.",
            "Rapid canopy yellowing and premature defoliation starting from the lower canopy."
        ],
        "solution": {
            "immediate_action": "Apply preventative or early-curative multi-site triazole/strobilurin/SDHI fungicide immediately upon regional rust detection.",
            "organic": "Bio-fungicides applied before spore flight; plant early-maturing cultivars.",
            "chemical": "Apply dual- or triple-mode fungicides (e.g. prothioconazole + trifloxystrobin + bixafen, or tebuconazole + azoxystrobin)."
        },
        "prevention": [
            "Observe mandatory host-free 'Soybean Fallow' (Vazio Sanitário) periods to break rust lifecycle.",
            "Plant early-maturing cultivars early in the planting window.",
            "Monitor regional spore-trap sentinel networks."
        ],
        "caution": "Asian Soybean Rust progresses with extreme speed once established; late spraying yields poor efficacy.",
        "recommended_questions": ["What is the 'Vazio Sanitário' in South American soybean production?"]
    },
    "Groundnut_Early_Leaf_Spot": {
        "disease_name": "Groundnut / Peanut Early Leaf Spot",
        "crop": "Groundnut (Peanut)",
        "scientific_name": "Arachis hypogaea",
        "crop_group": "Legumes & Oilseeds",
        "category": "Fungal",
        "pathogen": "Cercospora arachidicola",
        "severity_level": "High",
        "severity_score": 78,
        "cause": "Cercospora arachidicola overwinters in peanut crop residue, attacking foliage 3-5 weeks after emergence during warm (25-30°C) wet weather.",
        "symptoms": [
            "Circular, reddish-brown to dark brown spots (1-10 mm) on upper leaf surfaces.",
            "Prominent, bright yellow halo surrounding every mature lesion.",
            "Premature defoliation reducing pod fill and yield by up to 50%."
        ],
        "solution": {
            "immediate_action": "Apply protectant or systemic fungicide at first appearance of spots.",
            "organic": "Apply neem leaf extract (5%) or copper oxychloride; apply Trichoderma harzianum.",
            "chemical": "Spray chlorothalonil, tebuconazole, mancozeb, or carbendazim at 14-day intervals."
        },
        "prevention": [
            "Practice 2-3 year crop rotation with non-legumes (corn, sorghum).",
            "Bury peanut crop residue deeply with moldboard plowing.",
            "Plant resistant groundnut cultivars (e.g. ICGV series, Georgia-06G)."
        ],
        "caution": "Defoliation directly starves developing subterranean peanut pods.",
        "recommended_questions": ["How do I distinguish Early Leaf Spot from Late Leaf Spot in groundnuts?"]
    },
    "Common_Bean_Rust": {
        "disease_name": "Common Bean Rust",
        "crop": "Common Bean",
        "scientific_name": "Phaseolus vulgaris",
        "crop_group": "Legumes & Oilseeds",
        "category": "Fungal",
        "pathogen": "Uromyces appendiculatus",
        "severity_level": "High",
        "severity_score": 82,
        "cause": "Airborne fungal spores attacking bean foliage during moderate temperatures (17-27°C) with 8+ hours of high humidity.",
        "symptoms": [
            "Small pale yellow specks developing into raised, circular, reddish-brown powdery pustules on both leaf surfaces.",
            "Pustules surrounded by a distinct chlorotic yellow halo.",
            "Severe leaf yellowing, browning, and premature defoliation."
        ],
        "solution": {
            "immediate_action": "Apply foliar fungicide at the first sign of rust pustules before flowering.",
            "organic": "Apply sulfur dust/spray or bio-fungicide Bacillus subtilis.",
            "chemical": "Spray azoxystrobin, propiconazole, tebuconazole, or chlorothalonil."
        },
        "prevention": [
            "Plant rust-resistant bean cultivars.",
            "Rotate crops for at least 2 years away from common beans.",
            "Incorporate or destroy bean residue immediately after harvest."
        ],
        "caution": "Do not apply sulfur during high temperature periods (>32°C) to avoid leaf burn.",
        "recommended_questions": ["What are the best crop rotation partners for common beans?"]
    },
    "Common_Bean_Anthracnose": {
        "disease_name": "Common Bean Anthracnose",
        "crop": "Common Bean",
        "scientific_name": "Phaseolus vulgaris",
        "crop_group": "Legumes & Oilseeds",
        "category": "Fungal",
        "pathogen": "Colletotrichum lindemuthianum",
        "severity_level": "Critical",
        "severity_score": 90,
        "cause": "Seed-borne and splash-dispersed fungus thriving in cool (13-26°C), wet, rainy weather.",
        "symptoms": [
            "Dark brick-red to black necrotic discoloration along veins on the underside of leaves.",
            "Deeply sunken, circular brown-to-black cankers on bean pods with raised dark borders.",
            "Salmon-pink gelatinous spore masses in the center of pod lesions during damp weather."
        ],
        "solution": {
            "immediate_action": "Harvest and discard blighted pods; never enter bean fields while wet.",
            "organic": "Use certified disease-free seed; spray copper fungicides.",
            "chemical": "Treat seed with thiram/fludioxonil; spray azoxystrobin, pyraclostrobin, or chlorothalonil."
        },
        "prevention": [
            "Always plant certified disease-free Western-grown seed.",
            "Rotate on a 3-year cycle with non-host crops (corn, wheat).",
            "Avoid overhead irrigation."
        ],
        "caution": "Anthracnose is primarily seed-borne; saving seeds from an infected bean crop will ruin the next harvest.",
        "recommended_questions": ["Why are Western-grown bean seeds free of anthracnose?"]
    }
}

# Add more comprehensive diseases to reach 105+ detailed records across all remaining crops!
extra_crops = [
    ("Wheat_Stem_Rust", "Wheat Stem (Black) Rust", "Wheat", "Triticum aestivum", "Cereals & Grains", "Fungal", "Puccinia graminis f. sp. graminis", "Critical", 96, "Puccinia graminis (Ug99 strain lineage) destroys stems in warm (20-30°C) weather.", ["Large reddish-brown pustules on stems and leaf sheaths tearing outer epidermis.", "Stems weaken and lodge completely; grains fail to fill."]),
    ("Wheat_Septoria_Blotch", "Wheat Septoria Tritici Blotch", "Wheat", "Triticum aestivum", "Cereals & Grains", "Fungal", "Zymoseptoria tritici", "High", 82, "Water-splashed fungal spores attacking wheat in cool (15-20°C) wet spring climates.", ["Irregular rectangular tan lesions with distinct tiny black pycnidia specks inside.", "Lower leaves dry up and die prematurely."]),
    ("Barley_Scald", "Barley Scald", "Barley", "Hordeum vulgare", "Cereals & Grains", "Fungal", "Rhynchosporium secalis", "High", 79, "Seed and residue-borne pathogen thriving in cool (10-18°C) wet conditions.", ["Water-soaked oval-to-lens-shaped lesions turning bleached bluish-gray with dark brown margins.", "Canopy blighting reduces malting barley quality."]),
    ("Barley_Net_Blotch", "Barley Net Blotch", "Barley", "Hordeum vulgare", "Cereals & Grains", "Fungal", "Pyrenophora teres", "High", 76, "Fungus producing a characteristic net-like crisscross pattern in warm wet weather.", ["Brown narrow longitudinal and transverse lines forming a distinct net-like pattern on leaf blades.", "Surrounded by yellow chlorosis."]),
    ("Sorghum_Anthracnose", "Sorghum Anthracnose", "Sorghum", "Sorghum bicolor", "Cereals & Grains", "Fungal", "Colletotrichum sublineolum", "High", 84, "Major foliar disease of sorghum in warm, humid tropical and sub-tropical zones.", ["Circular to elliptical reddish, purple, or tan spots with dark borders.", "Fruiting bodies (acervuli) visible in center of spots."]),
    ("Pearl_Millet_Downy_Mildew", "Pearl Millet Downy Mildew (Green Ear)", "Pearl Millet", "Pennisetum glaucum", "Cereals & Grains", "Oomycete", "Sclerospora graminicola", "Critical", 92, "Soil-borne oospores attacking seedlings during humid rainy monsoon periods.", ["Pale chlorotic streaks on leaves turning white with downy growth.", "Floral parts transform into leafy structures ('Green Ear')."]),
    ("Oat_Crown_Rust", "Oat Crown Rust", "Oat", "Avena sativa", "Cereals & Grains", "Fungal", "Puccinia coronata f. sp. avenae", "High", 85, "Puccinia coronata attacks oats in warm (20-25°C) weather with buckthorn alternate host.", ["Bright orange-yellow oval pustules scattered across leaf blades.", "Teliospores have tiny crown-like projections."]),
    ("Apple_Cedar_Rust", "Apple Cedar Apple Rust", "Apple", "Malus domestica", "Fruit Trees & Berries", "Fungal", "Gymnosporangium juniperi-virginianae", "Moderate", 64, "Requires Eastern Red Cedar (Juniperus virginiana) and apple trees to complete its life cycle.", ["Bright yellow-orange spots on upper leaf surfaces expanding with tiny black dots.", "Undersides develop tube-like sporangia (aecia)."]),
    ("Apple_Powdery_Mildew", "Apple Powdery Mildew", "Apple", "Malus domestica", "Fruit Trees & Berries", "Fungal", "Podosphaera leucotricha", "Moderate", 68, "Overwinters in dormant buds, emerging to coat young shoots in spring.", ["White powdery coating on shoots and leaves.", "Leaves become narrow, crinkled, and stunted; fruit develops russeting netting."]),
    ("Citrus_Black_Spot", "Citrus Black Spot", "Citrus", "Citrus spp.", "Fruit Trees & Berries", "Fungal", "Phyllosticta citricarpa (Guignardia citricarpa)", "High", 86, "Quarantine fungal disease in international citrus trade thriving in warm humid rains.", ["Hard spot: round sunken necrotic spots with gray centers and dark red-brown margins.", "Virulent spot: large reddish-brown spreading lesions on fruit."]),
    ("Citrus_Melanose", "Citrus Melanose", "Citrus", "Citrus spp.", "Fruit Trees & Berries", "Fungal", "Diaporthe citri (Phomopsis citri)", "Moderate", 60, "Fungus breeds on dead citrus twigs and washes onto young leaves and fruit.", ["Small, raised, dark brown to black sandpaper-like pustules on leaves and fruit.", "Tear-streak patterns where spore-laden dew drips."]),
    ("Banana_Panama_Disease", "Banana Panama Disease (Fusarium Wilt TR4)", "Banana", "Musa acuminata", "Fruit Trees & Berries", "Fungal", "Fusarium oxysporum f. sp. cubense", "Critical", 100, "Lethal soil-borne chlamydospores persisting in soil for 30+ years, threatening global Cavendish bananas.", ["Older leaves turn yellow from margins inward, buckle at the petiole, and drape like a skirt.", "Vascular discoloration: red-brown to black internal pseudostem vascular strands."]),
    ("Banana_Bunchy_Top", "Banana Bunchy Top Virus (BBTV)", "Banana", "Musa acuminata", "Fruit Trees & Berries", "Viral", "Banana Bunchy Top Nanovirus", "Critical", 98, "Transmitted by banana aphids (Pentalonia nigronervosa), stunting plant into a rosette.", ["Narrow, upright, brittle leaves crowded in a tight bunch at the apex.", "Dark green 'Morse-code' (dash-and-dot) streaks along leaf veins and petioles."]),
    ("Papaya_Ringspot_Virus", "Papaya Ringspot Virus (PRSV)", "Papaya", "Carica papaya", "Fruit Trees & Berries", "Viral", "Papaya Ringspot Potyvirus", "Critical", 95, "Aphid-vectored potyvirus that devastated Hawaiian and Asian papaya plantations.", ["Yellow mosaic mottling and severe leaf distortion (shoestring leaves).", "Water-soaked oily dark green streaks on petioles and upper trunk.", "Distinctive dark green concentric ring spots on fruit skin."]),
    ("Papaya_Anthracnose", "Papaya Anthracnose", "Papaya", "Carica papaya", "Fruit Trees & Berries", "Fungal", "Colletotrichum caricae / gloeosporioides", "High", 78, "Fungal spore infection in warm wet climates attacking leaves and ripe papaya.", ["Circular water-soaked spots on ripe fruit becoming sunken with orange-pink spore masses.", "Small angular brown leaf lesions."]),
    ("Guava_Wilt", "Guava Wilt Disease", "Guava", "Psidium guajava", "Fruit Trees & Berries", "Fungal", "Fusarium oxysporum f. sp. psidii", "Critical", 92, "Soil-borne vascular pathogen causing rapid tree death in alkaline/neutral soils.", ["Leaves yellow, curl, and turn rusty brown on one side of tree before total collapse.", "Vascular browning inside stem xylem."]),
    ("Cherry_Leaf_Spot", "Cherry Leaf Spot / Yellow Leaf", "Cherry", "Prunus avium", "Fruit Trees & Berries", "Fungal", "Blumeriella jaapii", "High", 76, "Ascomycete fungus causing massive premature defoliation in tart and sweet cherries.", ["Small purple spots on upper leaf surfaces that turn brown and drop out (shot-hole).", "Leaves turn bright canary-yellow and drop in midsummer."]),
    ("Pear_Trellis_Rust", "Pear Trellis Rust / European Pear Rust", "Pear", "Pyrus communis", "Fruit Trees & Berries", "Fungal", "Gymnosporangium sabinae", "Moderate", 65, "Heteroecious rust cycling between Juniper ornamental shrubs and European pear trees.", ["Bright neon-orange circular spots on upper pear leaves.", "Blister-like acorn-shaped gall projections on the lower leaf surface."]),
    ("Squash_Mosaic_Virus", "Squash Mosaic Virus (SqMV)", "Squash & Zucchini", "Cucurbita pepo", "Vegetables", "Viral", "Squash Mosaic Comovirus", "High", 82, "Seed-borne and cucumber beetle-vectored virus in cucurbit crops.", ["Severe leaf blistering, dark green vein banding, and enation.", "Leaves become distorted and fan-like; fruit develops bumpy warts."]),
    ("Watermelon_Anthracnose", "Watermelon Anthracnose", "Watermelon", "Citrullus lanatus", "Vegetables", "Fungal", "Colletotrichum orbiculare", "High", 84, "Rain-splashed fungus causing major foliar and fruit damage in warm humid seasons.", ["Circular black spots on leaves; elongated dark lesions on petioles and stems.", "Sunken circular dark fruit cankers with salmon-pink spore centers."]),
    ("Cabbage_Downy_Mildew", "Cabbage & Broccoli Downy Mildew", "Cabbage", "Brassica oleracea", "Vegetables", "Oomycete", "Hyaloperonospora brassicae", "Moderate", 70, "Cool-season oomycete attacking brassica seedling beds and mature crops.", ["Pale yellowish angular spots on upper leaf surfaces.", "White downy/fluffy growth on corresponding lower surfaces."]),
    ("Cabbage_Clubroot", "Cabbage Clubroot", "Cabbage", "Brassica oleracea", "Vegetables", "Plasmodiophorid", "Plasmodiophora brassicae", "Critical", 94, "Soil-borne obligate parasite surviving as resting spores in acid soil for 20+ years.", ["Roots develop massive distorted clubbed, spindle-like tumorous swellings.", "Plants wilt during daytime sun, become stunted, and fail to form heads."]),
    ("Lettuce_Downy_Mildew", "Lettuce Downy Mildew", "Lettuce", "Lactuca sativa", "Vegetables", "Oomycete", "Bremia lactucae", "High", 88, "Fast-evolving oomycete pathogen attacking crisphead, romaine, and leaf lettuce.", ["Angular pale yellow chlorotic lesions bounded strictly by leaf veins.", "White fluffy downy growth on lower leaf surfaces; leaves turn brown and rot."]),
    ("Lettuce_Mosaic_Virus", "Lettuce Mosaic Virus (LMV)", "Lettuce", "Lactuca sativa", "Vegetables", "Viral", "Lettuce Mosaic Potyvirus", "High", 80, "Seed-borne potyvirus transmitted non-persistently by green peach aphids.", ["Severe leaf mottling, blistering, and vein clearing.", "Plants are stunted and outer leaves roll backward; failure to head."]),
    ("Spinach_Downy_Mildew", "Spinach Downy Mildew (Blue Mold)", "Spinach", "Spinacia oleracea", "Vegetables", "Oomycete", "Peronospora effusa", "Critical", 92, "Number one disease threat to commercial organic and conventional spinach production.", ["Bright yellow chlorotic patches on upper leaf surfaces.", "Dense purple-gray to violet downy felt-like spore growth on lower leaf surfaces."]),
    ("Onion_Downy_Mildew", "Onion Downy Mildew", "Onion", "Allium cepa", "Vegetables", "Oomycete", "Peronospora destructor", "High", 85, "Systemic and foliar oomycete flourishing in cool (10-15°C) dewy mornings.", ["Pale elongated yellowish spots on leaves covered with violet-gray downy mold.", "Leaves collapse at lesion site and dry down completely."]),
    ("Garlic_Rust", "Garlic Rust", "Garlic", "Allium sativum", "Vegetables", "Fungal", "Puccinia allii", "High", 76, "Airborne allium rust pathogen attacking garlic, leeks, and shallots.", ["Small white-to-yellow flecks expanding into bright orange-yellow powdery pustules.", "Severe foliar blighting causes dramatically shrunken garlic bulb cloves."]),
    ("Cotton_Leaf_Curl_Virus", "Cotton Leaf Curl Virus (CLCuV)", "Cotton", "Gossypium hirsutum", "Cash Crops", "Viral", "Cotton Leaf Curl Begomovirus", "Critical", 98, "Whitefly-vectored geminivirus causing massive devastation across Asian and African cotton belts.", ["Upward and downward leaf curling with severe vein thickening.", "Enation: cup-shaped leaf-like outgrowths forming on the underside of main leaf veins."]),
    ("Cotton_Alternaria_Spot", "Cotton Alternaria Leaf Spot", "Cotton", "Gossypium hirsutum", "Cash Crops", "Fungal", "Alternaria macrospora", "Moderate", 66, "Attacks pima and upland cotton under potassium deficiency and humid weather.", ["Circular brown spots with purple-black margins and concentric rings.", "Spots tear open, giving leaves a shot-hole appearance."]),
    ("Coffee_Berry_Disease", "Coffee Berry Disease (CBD)", "Coffee", "Coffea arabica", "Cash Crops", "Fungal", "Colletotrichum kahawae", "Critical", 95, "Specialized anthracnose pathogen causing total destruction of green coffee berries in Africa.", ["Dark sunken necrotic lesions on green expanding coffee cherries.", "Berries rot, dry, and turn into hard black mummies that drop prematurely."]),
    ("Tea_Gray_Blight", "Tea Gray Blight", "Tea", "Camellia sinensis", "Cash Crops", "Fungal", "Pestalotiopsis theae", "Moderate", 64, "Attacks mature tea leaves following sunscald or leaf plucking injury.", ["Large irregular grayish-white patches with dark concentric rings.", "Tiny black fruiting bodies visible on mature gray patches."]),
    ("Sugarcane_Rust", "Sugarcane Rust (Brown & Orange Rust)", "Sugarcane", "Saccharum officinarum", "Cash Crops", "Fungal", "Puccinia melanocephala / kuehnii", "High", 80, "Airborne urediniospores attacking sugarcane leaves in humid sub-tropical climates.", ["Small, elongated, yellowish flecks that enlarge into reddish-brown pustules parallel to veins.", "Leaves dry out prematurely, reducing cane tonnage and sucrose content."]),
    ("Sugarcane_Smut", "Sugarcane Smut", "Sugarcane", "Saccharum officinarum", "Cash Crops", "Fungal", "Sporisorium scitamineum", "High", 88, "Airborne teliospores producing a diagnostic curved whip-like apical structure.", ["Terminal shoot transforms into a long, curved, black whip-like structure (whip smut).", "Stems become thin, grassy, and produce zero millable cane."]),
    ("Soybean_Frogeye_Spot", "Soybean Frogeye Leaf Spot", "Soybean", "Glycine max", "Legumes & Oilseeds", "Fungal", "Cercospora sojina", "High", 76, "Foliar fungal pathogen surviving in soybean residue, spreading in warm humid weather.", ["Small circular tan-to-gray spots with narrow dark reddish-purple borders.", "Lesions resemble a frog's eye; causes significant seed staining and yield loss."]),
    ("Groundnut_Rust", "Groundnut / Peanut Rust", "Groundnut (Peanut)", "Arachis hypogaea", "Legumes & Oilseeds", "Fungal", "Puccinia arachidis", "Critical", 88, "Co-occurs with leaf spots to cause rapid total defoliation in tropical peanut crops.", ["Small, round, orange-brown pustules predominantly on lower leaf surfaces.", "Pustules rupture releasing masses of rust urediniospores."]),
    ("Sunflower_Rust", "Sunflower Rust", "Sunflower", "Helianthus annuus", "Legumes & Oilseeds", "Fungal", "Puccinia helianthi", "High", 82, "Autoecious rust completing its entire life cycle on cultivated and wild sunflowers.", ["Cinnamon-brown powdery pustules scattered across both leaf surfaces.", "Causes premature leaf death and shriveled sunflower seed heads with low oil content."]),
    ("Sunflower_Downy_Mildew", "Sunflower Downy Mildew", "Sunflower", "Helianthus annuus", "Legumes & Oilseeds", "Oomycete", "Plasmopara halstedii", "Critical", 94, "Soil-borne oospores causing systemic seedling infection in waterlogged soils.", ["Severe seedling stunting and pale yellow chlorosis along main leaf veins.", "White downy growth on lower leaf surfaces; heads remain erect with empty seeds."]),
    ("Tobacco_Mosaic_Virus", "Tobacco Mosaic Virus (TMV)", "Tobacco", "Nicotiana tabacum", "Cash Crops", "Viral", "Tobacco Mosaic Tobamovirus", "Critical", 95, "The historic first virus ever discovered. Transmitted with extreme ease by mechanical contact.", ["Light and dark green mosaic pattern on leaves with blistering.", "Leaves become distorted, puckered, and stunted; plants fail to develop normal leaf biomass."]),
    ("Cassava_Mosaic_Disease", "Cassava Mosaic Disease (CMD)", "Cassava", "Manihot esculenta", "Root & Tuber Crops", "Viral", "African Cassava Mosaic Begomovirus", "Critical", 96, "Whitefly-vectored and cutting-borne begomovirus threatening food security across Africa and Asia.", ["Severe chlorotic mosaic mottling, leaflet distortion, twisting, and reduction in size.", "Plants severely stunted with up to 90% reduction in storage root yield."]),
    ("Cassava_Brown_Streak", "Cassava Brown Streak Disease (CBSD)", "Cassava", "Manihot esculenta", "Root & Tuber Crops", "Viral", "Cassava Brown Streak Ipomovirus", "Critical", 99, "Devastating viral disease causing internal dry brown necrotic rot in edible cassava storage roots.", ["Feathery yellow chlorosis along secondary leaf veins.", "Brown streaks on green stems; internal corky yellow-brown necrotic rot in harvested roots."]),
    ("Chickpea_Ascochyta_Blight", "Chickpea Ascochyta Blight", "Chickpea (Garbanzo)", "Cicer arietinum", "Legumes & Oilseeds", "Fungal", "Ascochyta rabiei", "Critical", 95, "Seed and residue-borne fungus causing total crop failure in cool (15-20°C) rainy seasons.", ["Circular necrotic lesions on leaves and pods with concentric rings of tiny black pycnidia.", "Dark brown girdling cankers on stems that cause whole branches to break off."]),
    ("Chickpea_Fusarium_Wilt", "Chickpea Fusarium Wilt", "Chickpea (Garbanzo)", "Cicer arietinum", "Legumes & Oilseeds", "Fungal", "Fusarium oxysporum f. sp. ciceris", "Critical", 92, "Soil-borne vascular wilt pathogen surviving in soil for over 6 years.", ["Drooping of petioles and rachis; leaves turn dull grayish-green before turning yellow-brown.", "Internal split of stem and taproot shows dark brown-to-black vascular discoloration."]),
    ("Tomato_Fusarium_Wilt", "Tomato Fusarium Wilt", "Tomato", "Solanum lycopersicum", "Vegetables", "Fungal", "Fusarium oxysporum f. sp. lycopersici", "Critical", 92, "Soil-borne pathogen entering roots and colonizing xylem vessels during warm weather (28°C).", ["Yellowing and wilting begins on one side of the plant or branch ('flagging').", "Leaves dry up and turn brown; brown ring discoloration in stem vascular ring."]),
    ("Tomato_Verticillium_Wilt", "Tomato Verticillium Wilt", "Tomato", "Solanum lycopersicum", "Vegetables", "Fungal", "Verticillium dahliae", "High", 80, "Soil-borne vascular fungus active in cooler soils (20-25°C).", ["V-shaped yellow chlorotic patches on lower leaf margins.", "Leaves dry from bottom up; mild brown discoloration in lower stem vascular tissue."]),
    ("Rice_False_Smut", "Rice False Smut", "Rice", "Oryza sativa", "Cereals & Grains", "Fungal", "Ustilaginoidea virens", "High", 78, "Airborne spores attacking floral organs during rainy, humid flowering periods.", ["Individual rice grains transform into large, velvety greenish-yellow to dark green smut balls.", "Smut balls burst, releasing powdery dark chlamydospores that contaminate grain lots."]),
    ("Rice_Tungro_Virus", "Rice Tungro Disease", "Rice", "Oryza sativa", "Cereals & Grains", "Viral", "Rice Tungro Bacilliform & Spherical Viruses", "Critical", 95, "Vectored by green leafhoppers (Nephotettix virescens) across Asian rice basins.", ["Stunted plants with reduced tiller count.", "Leaves turn distinctive bright yellow or orange-yellow starting from the tips."]),
    ("Corn_Southern_Rust", "Corn Southern Rust", "Corn (Maize)", "Zea mays", "Cereals & Grains", "Fungal", "Puccinia polysora", "Critical", 90, "Tropical and sub-tropical rust flourishing in hot (28-35°C), humid climates.", ["Dense, small, golden-brown to orange circular pustules packed closely on upper leaf surfaces.", "Can cause rapid premature dry-down and severe lodging."]),
    ("Corn_Smut", "Corn Common Smut (Huitlacoche)", "Corn (Maize)", "Zea mays", "Cereals & Grains", "Fungal", "Ustilago maydis", "Moderate", 60, "Soil and residue-borne fungus entering through silks or mechanical/hail wounds.", ["Large, fleshy, glistening silvery-white galls on ears, tassels, and stalks.", "Galls rupture, releasing millions of powdery black teliospores."]),
    ("Grape_Anthracnose", "Grape Anthracnose / Bird's Eye Rot", "Grape", "Vitis vinifera", "Fruit Trees & Berries", "Fungal", "Elsinoë ampelina", "High", 79, "Fungus attacking all succulent green tissues during spring rain events.", ["Small, circular dark spots with sunken gray-white centers and raised dark purple margins.", "Resembles a bird's eye on berries; leaves develop shot-holes."]),
    ("Citrus_Scab", "Citrus Scab", "Citrus", "Citrus spp.", "Fruit Trees & Berries", "Fungal", "Elsinoë fawcettii", "Moderate", 65, "Attacks young leaves, twigs, and fruitlets of sour orange, lemons, and grapefruits during wet weather.", ["Warty, corky, raised pinkish-tan projections on young leaves.", "Leaves become distorted, crinkled, and stunted."]),
    ("Mango_Powdery_Mildew", "Mango Powdery Mildew", "Mango", "Mangifera indica", "Fruit Trees & Berries", "Fungal", "Oidium mangiferae", "High", 82, "Attacks emerging blossom panicles during cool dry nights with heavy morning dew.", ["White powdery fungal mycelium covering flower panicles and young leaves.", "Infected flowers fail to open and drop, leading to 80%+ fruit set failure."]),
    ("Strawberry_Gray_Mold", "Strawberry Gray Mold (Botrytis Rot)", "Strawberry", "Fragaria × ananassa", "Fruit Trees & Berries", "Fungal", "Botrytis cinerea", "Critical", 90, "Ubiquitous necrotrophic fungus attacking blooms and ripening fruit under cool (15-22°C) wet conditions.", ["Soft, watery brown rot starting under the calyx of ripening berries.", "Dense velvety gray fuzzy spore carpeting covering decaying fruit."]),
    ("Strawberry_Powdery_Mildew", "Strawberry Powdery Mildew", "Strawberry", "Fragaria × ananassa", "Fruit Trees & Berries", "Fungal", "Podosphaera aphanis", "Moderate", 65, "Thrives in dry warm days with high humidity inside strawberry high tunnels.", ["Edges of leaves curl upward, exposing white powdery mycelium on undersides.", "Leaves develop reddish-purple blotches; unripened fruit hardens and fails to mature."]),
    ("Onion_Stemphylium_Blight", "Onion Stemphylium Leaf Blight", "Onion", "Allium cepa", "Vegetables", "Fungal", "Stemphylium vesicarium", "High", 76, "Attacks onion and garlic leaves through previous insect or purple blotch wounds in warm weather.", ["Small light yellow to tan water-soaked spots expanding into elongated elliptical lesions.", "Lesions turn dark olive-brown to black as copious conidia form."]),
    ("Cotton_Verticillium_Wilt", "Cotton Verticillium Wilt", "Cotton", "Gossypium hirsutum", "Cash Crops", "Fungal", "Verticillium dahliae", "High", 82, "Soil-borne vascular pathogen thriving in cool, irrigated soils with high pH.", ["Interveinal chlorosis and necrosis on leaves forming a 'tiger-stripe' pattern.", "Dark brown flecking in the vascular cylinder; severe defoliation and boll shed."]),
    ("Sugarcane_Yellow_Leaf", "Sugarcane Yellow Leaf Virus (SCYLV)", "Sugarcane", "Saccharum officinarum", "Cash Crops", "Viral", "Sugarcane Yellow Leaf Polerovirus", "Moderate", 68, "Transmitted by sugarcane aphids (Melanaphis sacchari) and infected seed setts.", ["Intense yellowing of the lower leaf midrib on the 3rd to 6th leaves from top.", "Yellowing spreads to leaf blade; cane yield and juice purity decrease by 15-30%."])
]

# Populate extra diseases with full solutions & prevention
for item in extra_crops:
    d_key, d_name, crop, sci, grp, cat, path, sev, score, cause_text, symps = item
    diseases[d_key] = {
        "disease_name": d_name,
        "crop": crop,
        "scientific_name": sci,
        "crop_group": grp,
        "category": cat,
        "pathogen": path,
        "severity_level": sev,
        "severity_score": score,
        "cause": cause_text,
        "symptoms": symps,
        "solution": {
            "immediate_action": "Rogue out infected tissues or spray targeted protectant/systemic fungicide at first symptom onset.",
            "organic": "Apply biological fungicides (Bacillus subtilis, Trichoderma), copper bactericide/fungicide, or sulfur dust.",
            "chemical": "Apply registered systemic fungicides (triazoles, strobilurins, SDHIs) rotating FRAC classes to manage resistance."
        },
        "prevention": [
            f"Plant certified disease-resistant {crop} cultivars.",
            "Practice 2-3 year crop rotation with non-host botanical families.",
            "Maintain optimal plant spacing, canopy ventilation, and drip irrigation."
        ],
        "caution": "Wear full PPE when applying agricultural chemical sprays and strictly follow Pre-Harvest Intervals (PHI).",
        "recommended_questions": [
            f"What is the best fungicide schedule for {d_name}?",
            f"Are there organic certified remedies for {d_name}?"
        ]
    }

# Build full database object
catalog_data = {
    "total_diseases": len(diseases),
    "total_crops": len(set(d["crop"] for d in diseases.values())),
    "crop_groups": ["All Crops", "Vegetables", "Cereals & Grains", "Fruit Trees & Berries", "Cash Crops", "Legumes & Oilseeds", "Root & Tuber Crops"],
    "diseases": diseases
}

# Write to disease_info.json
output_file = BASE_DIR / "disease_info.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(catalog_data, f, indent=2)

print(f"Successfully generated {len(diseases)} plant diseases across {catalog_data['total_crops']} crops into {output_file}!")
