"""
PlantVision AI - Agentic Plant Health Assistant
Context-aware intelligent agent for plant disease diagnosis, treatment workflows,
organic/chemical action plans, and conversational human-like plant health management.
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger("PlantVision.AgentService")


class PlantHealthAgent:
    """
    Agentic AI Plant Health Assistant that provides:
    - Contextual reasoning around diagnosed plant leaf scans
    - Human-like conversational botanical advice & empathy
    - Step-by-step immediate treatment action plans
    - Organic vs chemical recipe dosage guidelines
    - Watering, soil, nutrition, pruning, and pest management
    - Contagion risk assessment and quarantine advice
    - Preventative cultural schedules and monitoring tasks
    - Dynamic follow-up question suggestions
    """

    def __init__(self, disease_info_path: Optional[str] = None):
        workspace_root = Path(__file__).resolve().parent.parent
        self.disease_info_path = Path(disease_info_path) if disease_info_path else workspace_root / "disease_info.json"
        self.disease_info = self._load_disease_info()

    def _load_disease_info(self) -> Dict[str, Any]:
        if self.disease_info_path.exists():
            try:
                with open(self.disease_info_path, "r", encoding="utf-8") as f:
                    return json.load(f).get("diseases", {})
            except Exception as e:
                logger.error(f"Failed to load disease_info: {e}")
        return {}

    def generate_response(
        self,
        question: str,
        scan_context: Optional[Dict[str, Any]] = None,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Processes a user question, incorporates current leaf scan context if available,
        and generates structured agentic guidance, actionable steps, and suggested follow-ups.
        """
        q_raw = question.strip()
        q_lower = q_raw.lower()
        
        context_disease = scan_context.get("disease") if scan_context else None
        context_crop = scan_context.get("crop") if scan_context else None
        context_severity = scan_context.get("severity") if scan_context else None
        context_id = scan_context.get("disease_id") if scan_context else None

        # Look up disease knowledge if context exists or if mentioned in question
        matched_disease_key = None
        matched_info = {}

        if context_id and context_id in self.disease_info:
            matched_disease_key = context_id
            matched_info = self.disease_info[context_id]
        else:
            # Try to match query keywords with disease repository
            for k, info in self.disease_info.items():
                d_name = info.get("disease_name", "").lower()
                c_name = info.get("crop", "").lower()
                if (c_name in q_lower and any(w in q_lower for w in ["blight", "rust", "spot", "scab", "mold", "rot", "mildew", "mosaic", "curl", "mite", "scorch"])) or d_name in q_lower:
                    matched_disease_key = k
                    matched_info = info
                    break

        # Fallback to context info if provided
        if not matched_info and scan_context:
            matched_info = {
                "disease_name": context_disease,
                "crop": context_crop,
                "severity_level": context_severity or "Moderate",
                "cause": scan_context.get("cause", ""),
                "solution": scan_context.get("solution", {}),
                "prevention": scan_context.get("prevention", []),
                "caution": scan_context.get("caution", "")
            }

        disease_name = matched_info.get("disease_name", context_disease or "Plant Disease")
        crop = matched_info.get("crop", context_crop or "Plant")
        severity = matched_info.get("severity_level", "Moderate")
        solution_data = matched_info.get("solution", {})
        organic_sol = solution_data.get("organic", "Apply organic bio-fungicide, neem oil, or copper spray.") if isinstance(solution_data, dict) else str(solution_data)
        chemical_sol = solution_data.get("chemical", "Apply broad-spectrum registered fungicide according to label directions.") if isinstance(solution_data, dict) else ""
        cause_text = matched_info.get("cause", "Fungal, bacterial, or environmental stress.")
        prevention_list = matched_info.get("prevention", ["Maintain proper airflow, bottom watering, and crop rotation."])
        caution_text = matched_info.get("caution", "Wear protective gloves and wash hands after handling diseased foliage.")

        has_scan = bool(context_disease and context_disease != "Plant Disease" and context_disease != "Healthy")

        # =========================================================================
        # 1. "WHAT QUESTIONS CAN I ASK ABOUT A PLANT?" (Comprehensive Guide)
        # =========================================================================
        if any(term in q_lower for term in [
            "what are the question", "what questions", "what can i ask", "how to ask",
            "questions we ask", "questions to ask", "help", "guide", "what should i ask",
            "example questions", "list questions", "topics", "options"
        ]):
            answer = (
                f"🌿 **Hello! I am your AI Agronomist & Botanical Doctor.** You can speak or chat with me about *any* aspect of plant care, gardening, and crop health!\n\n"
                f"Here are the most valuable and common questions you can ask me:\n\n"
                f"### 🔍 1. Diagnosis & Leaf Symptoms\n"
                f"- *\"Why are my leaves turning yellow, brown, or curling?\"*\n"
                f"- *\"What are these white powdery spots or dark rings on my foliage?\"*\n"
                f"- *\"How do I know if my plant is infected with fungal blight or bacteria?\"*\n\n"
                f"### 🥣 2. Organic & Homemade DIY Remedies\n"
                f"- *\"How do I make a baking soda and neem oil spray recipe?\"*\n"
                f"- *\"Can I use a milk and water foliar spray for powdery mildew?\"*\n"
                f"- *\"What is the best natural bio-fungicide for vegetable gardens?\"*\n\n"
                f"### 🧪 3. Chemical Treatments & Fungicide Schedules\n"
                f"- *\"What chemical fungicide is most effective and how often do I spray?\"*\n"
                f"- *\"How do I rotate fungicide FRAC groups to prevent pathogen resistance?\"*\n\n"
                f"### 💧 4. Watering, Soil & Root Health\n"
                f"- *\"How often should I water my plants, and how do I avoid root rot?\"*\n"
                f"- *\"What are the clear signs of overwatering versus underwatering?\"*\n\n"
                f"### 🌱 5. Fertilizer & Plant Nutrition (N-P-K)\n"
                f"- *\"What fertilizer ratio is best for vegetative growth vs flowering?\"*\n"
                f"- *\"How do I fix nitrogen, iron, or calcium deficiency (like blossom end rot)?\"*\n\n"
                f"### 🐛 6. Pests & Natural Insect Control\n"
                f"- *\"How do I eliminate aphids, spider mites, and whiteflies naturally?\"*\n"
                f"- *\"How do I make a safe homemade insecticidal soap?\"*\n\n"
                f"### ☀️ 7. Sunlight, Climate & Pruning Care\n"
                f"- *\"How much direct sunlight does my plant need?\"*\n"
                f"- *\"When and how should I prune lower diseased foliage safely?\"*\n\n"
                f"### 🍎 8. Harvest Safety, Edibility & Quarantine\n"
                f"- *\"Can I safely eat the fruit or harvest from a diseased plant?\"*\n"
                f"- *\"Will this disease spread to other crops, and how do I quarantine it?\"*\n\n"
                f"💡 *Tip: You can click 🎙️ to talk aloud using your microphone, or choose any topic below!*"
            )
            suggested_follow_ups = [
                "Why are my leaves turning yellow?",
                "How do I make a homemade organic spray?",
                "How often should I water my plants?",
                "How do I get rid of pests naturally?"
            ]

        # =========================================================================
        # 2. GREETINGS & PERSONAL SMALL TALK (Warm, Empathetic Human Tone)
        # =========================================================================
        elif any(q_lower.startswith(g) for g in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "howdy", "greetings", "sup"]):
            if has_scan:
                answer = (
                    f"👋 **Hello there!** I'm your PlantVision AI Health Companion. It's wonderful to connect with you!\n\n"
                    f"I see we currently have a scan for **{disease_name}** on your **{crop}**. Don't worry—plants are remarkably resilient, and together we can nurse yours back to vibrant health.\n\n"
                    f"How can I help you right now? We can explore an organic spray recipe, chemical fungicide rotation, quarantine steps, or watering advice!"
                )
            else:
                answer = (
                    f"👋 **Hello! Welcome to PlantVision AI.** I am your friendly AI Agronomist & Botanical Doctor.\n\n"
                    f"I love talking with plant parents and growers! Whether you have a sick garden crop, yellowing indoor houseplant, mystery leaf spots, or just want watering tips, I'm here to talk through it with you.\n\n"
                    f"What's on your mind today regarding your plants?"
                )
            suggested_follow_ups = [
                "What questions can I ask about a plant?",
                "Why are my plant leaves turning yellow?",
                "What is a good multi-purpose organic foliar spray?"
            ]

        # 2.1 Gratitude & Kindness
        elif any(term in q_lower for term in ["thank you", "thanks", "appreciate", "helpful", "awesome", "great job", "you are the best", "you are awesome"]):
            answer = (
                f"🌱 **You are so very welcome!** It truly makes my day to help you and your plants flourish.\n\n"
                f"Gardening is both a science and a labor of love. Every leaf you nurture makes the world greener! If you ever notice any new spots, wilting, or need feeding tips, I'm always right here for you.\n\n"
                f"Would you like to review preventive measures or check anything else for your garden today?"
            )
            suggested_follow_ups = [
                f"What preventive steps should I take next season for {crop}?",
                "How often should I inspect my foliage?",
                "What is a natural fertilizer to boost plant immunity?"
            ]

        # 2.2 Identity & Assistant Bio
        elif any(term in q_lower for term in ["who are you", "what are you", "what can you do", "tell me about yourself", "your name"]):
            answer = (
                f"🌿 **I am PlantVision AI**—your dedicated AI Agronomist, Plant Pathologist, and Botanical Voice Companion!\n\n"
                f"Here is how I can assist you:\n"
                f"1. **Voice Conversation:** You can speak with me using your microphone, and I will speak back to you with natural voice audio.\n"
                f"2. **Leaf Scan Analysis:** Diagnose 115+ crop diseases with deep pathology insights.\n"
                f"3. **Prescriptive Action Plans:** Provide custom Organic DIY recipes, Synthetic Fungicide schedules, and Quarantine protocols.\n"
                f"4. **Holistic Plant Care:** Troubleshoot watering, soil drainage, sunlight, fertilizers (N-P-K), pruning, and organic pest eradication."
            )
            suggested_follow_ups = [
                "What questions can I ask about a plant?",
                "How do I make a homemade organic spray?",
                "How do I prevent root rot in potted plants?"
            ]

        # 2.3 General How Are You
        elif any(term in q_lower for term in ["how are you", "how's it going", "how are you doing", "how do you feel"]):
            answer = (
                f"😊 **I'm doing wonderful and thriving, thank you for asking!** Just like a well-watered seedling in the morning sun, I'm fully energized and ready to help you.\n\n"
                f"How is your garden or plant collection doing today? Are your leaves looking green and happy, or are you noticing any spots or wilting?"
            )
            suggested_follow_ups = [
                "Why are my plant leaves turning yellow?",
                "What is the best way to water plants?",
                "What organic spray can I prepare at home?"
            ]

        # =========================================================================
        # 3. LEAF SYMPTOMS (Yellowing, Browning, Curling, Wilting, Drooping, Spots)
        # =========================================================================
        elif any(term in q_lower for term in [
            "yellow", "yellowing", "brown", "browning", "curl", "curling",
            "wilt", "wilting", "droop", "drooping", "spots", "black spot", "dry tip",
            "leaf drop", "falling leaves", "dying", "sick plant", "white powder"
        ]):
            if has_scan:
                answer = (
                    f"🌿 **Let's diagnose what your {crop} is experiencing with {disease_name}:**\n\n"
                    f"### 🔍 Symptom Breakdown\n"
                    f"- **Visual Lesions:** {cause_text}\n"
                    f"- **Severity Level:** **{severity}**\n\n"
                    f"### 🩺 What Causes These Symptoms?\n"
                    f"1. **Pathogenic Stress:** Microscopic spores germinate when water lingers on the leaf surface, causing cell tissue collapse (manifested as yellow halos, brown necrotic centers, or curling margins).\n"
                    f"2. **Water Imbalance:** Inconsistent watering weakens the plant's natural immune barriers.\n"
                    f"3. **Nutrient Blockage:** Infected vascular bundles prevent nitrogen and magnesium from reaching the upper canopy.\n\n"
                    f"### 🛠️ Immediate First Aid Steps:\n"
                    f"1. **Prune Lower Damaged Leaves:** Remove heavily spotted or yellowed foliage using alcohol-sterilized shears.\n"
                    f"2. **Switch to Bottom/Soil Watering:** Never splash water onto the leaves.\n"
                    f"3. **Apply First Response Remedy:** {organic_sol}"
                )
            else:
                answer = (
                    f"🌿 **I completely understand your concern! Seeing leaves turn yellow, brown, or droop is stressful, but we can fix this.**\n\n"
                    f"Here is how a plant doctor identifies the root cause:\n\n"
                    f"### 1. Yellowing Leaves (Chlorosis)\n"
                    f"- **Bottom leaves yellowing & soft:** Usually **Overwatering** (suffocating roots) or **Nitrogen deficiency**.\n"
                    f"- **Yellowing between veins (veins stay green):** **Iron or Magnesium deficiency**.\n"
                    f"- **Yellowing with spots/halos:** **Fungal or Bacterial leaf spot**.\n\n"
                    f"### 2. Brown, Crispy Tips & Edges\n"
                    f"- **Crisp brown margins:** **Underwatering**, low humidity, or excess fertilizer salt accumulation.\n"
                    f"- **Brown spots with yellow rings:** Active fungal pathogen (e.g. Blight or Rust).\n\n"
                    f"### 3. Curling or Drooping Leaves\n"
                    f"- **Curling upward + dry soil:** Heat stress or thirst (the plant is conserving water).\n"
                    f"- **Drooping with wet soggy soil:** Root rot (damaged roots cannot take up oxygen).\n\n"
                    f"💡 *Would you like to scan a leaf using our scanner, or should we prepare an organic foliar spray?*"
                )
            suggested_follow_ups = [
                "How do I know if I am overwatering or underwatering?",
                "What homemade organic spray can I prepare?",
                "How do I fix nitrogen deficiency in plants?"
            ]

        # =========================================================================
        # 4. WATERING, SOIL MOISTURE, DRAINAGE & ROOT ROT
        # =========================================================================
        elif any(term in q_lower for term in [
            "water", "watering", "how often to water", "overwater", "underwater",
            "soil", "drainage", "moisture", "root rot", "soggy", "wet soil", "dry soil"
        ]):
            answer = (
                f"💧 **Mastering watering is the #1 secret to healthy, disease-free plants!** Here is the complete agronomist guide for **{crop if has_scan else 'your plants'}**:\n\n"
                f"### 📏 1. The Golden 'Finger Test' Rule\n"
                f"- Insert your index finger **2 inches (5 cm)** into the soil.\n"
                f"- If it feels **dry and warm**, it's time to water thoroughly.\n"
                f"- If it feels **cool and damp**, wait 1 to 2 more days before checking again.\n\n"
                f"### ☀️ 2. Time of Day & Technique\n"
                f"- **Always water early in the morning:** This allows any accidental splashes on foliage to evaporate in the morning sun, preventing fungal spores from germinating.\n"
                f"- **Water the Soil, Not the Leaves:** Direct the spout or drip line at the base of the stem.\n\n"
                f"### 🛑 3. Overwatering vs Underwatering Comparison\n"
                f"- **Overwatering Signs:** Soggy soil, yellowing lower leaves that feel soft/limp, musty soil smell, fungus gnats, root rot.\n"
                f"- **Underwatering Signs:** Bone-dry soil pulling away from the pot edge, crispy brown leaf tips, upward leaf curl.\n\n"
                f"### 🩺 4. How to Cure Root Rot & Improve Drainage\n"
                f"- **Soil Drainage:** Ensure pots have adequate drainage holes and amend heavy clay soils with **perlite, coarse sand, or pumice**.\n"
                f"- Let the top 2-3 inches of soil dry completely.\n"
                f"- Drench the soil with a gentle solution of **1 tablespoon 3% Hydrogen Peroxide per 1 cup of water** to inject oxygen into the root zone and kill anaerobic bacteria."
            )
            suggested_follow_ups = [
                "How do I improve soil drainage for potted plants?",
                "What is a natural fertilizer to strengthen roots?",
                "Why are my plant leaves turning yellow?"
            ]

        # =========================================================================
        # 5. FERTILIZER, N-P-K & PLANT NUTRITION
        # =========================================================================
        elif any(term in q_lower for term in [
            "fertilizer", "fertilize", "feed", "feeding", "npk", "nitrogen",
            "phosphorus", "potassium", "calcium", "magnesium", "compost", "nutrient", "yellow vein"
        ]):
            answer = (
                f"🌱 **Proper plant nutrition is like a strong immune system for your crops!** Here is how to feed **{crop if has_scan else 'your garden'}** effectively:\n\n"
                f"### 🧪 1. Understanding N-P-K Numbers\n"
                f"- **N (Nitrogen):** Drives lush, leafy green growth. *Deficiency sign:* Overall pale yellow lower leaves.\n"
                f"- **P (Phosphorus):** Stimulates strong root systems, flower blooming, and fruit set. *Deficiency sign:* Stunted growth and purplish leaf tints.\n"
                f"- **K (Potassium):** Enhances disease resistance, water regulation, and cold tolerance. *Deficiency sign:* Yellowing or scorching along leaf margins.\n\n"
                f"### 🥛 2. Crucial Micronutrients (Calcium & Magnesium)\n"
                f"- **Calcium Deficiency:** Causes **Blossom End Rot** (sunken black bottoms on tomatoes and peppers). Add agricultural gypsum or crushed eggshell powder.\n"
                f"- **Magnesium Deficiency:** Causes interveinal yellowing. Spray a foliar solution of **1 tablespoon Epsom Salt per gallon of water**.\n\n"
                f"### 🥣 3. Organic Soil Boosters\n"
                f"- Top-dress with **aged compost or worm castings** every 4 to 6 weeks.\n"
                f"- Apply **liquid kelp or fish emulsion** for gentle micronutrient uptake.\n\n"
                f"⚠️ *Golden Rule: Never heavily fertilize a plant that is severely wilted, heat-stressed, or actively battling severe root rot.*"
            )
            suggested_follow_ups = [
                "How do I prevent blossom end rot in tomatoes?",
                "How do I make organic compost tea at home?",
                "How often should I water my plants?"
            ]

        # =========================================================================
        # 6. PESTS & NATURAL INSECT CONTROL
        # =========================================================================
        elif any(term in q_lower for term in [
            "pest", "pests", "bug", "bugs", "insect", "insects", "aphid", "aphids",
            "spider mite", "mites", "whitefly", "whiteflies", "thrips", "caterpillar",
            "worm", "scale", "mealybug", "beetle", "slug", "snail"
        ]):
            answer = (
                f"🐛 **Let's protect your garden from pests naturally!** Here is your organic pest eradication battle plan for **{crop if has_scan else 'your crops'}**:\n\n"
                f"### 🧼 1. Homemade Organic Insecticidal Soap Recipe\n"
                f"- **Ingredients:**\n"
                f"  • 1 tablespoon mild liquid Castile soap (unscented)\n"
                f"  • 1 tablespoon pure cold-pressed neem oil or horticultural oil\n"
                f"  • 1 quart (1 Liter) of warm water\n"
                f"- **Application:** Shake well and spray directly onto insects—especially on the **undersides of leaves** and stem joints. Repeat every 3 to 5 days.\n\n"
                f"### 🎯 2. Pest-Specific Solutions\n"
                f"- **Aphids & Spider Mites:** Blast them off with a firm jet of water from your hose, then spray with neem oil solution.\n"
                f"- **Whiteflies & Fungus Gnats:** Hang yellow sticky traps around the canopy and let topsoil dry out.\n"
                f"- **Caterpillars & Hornworms:** Hand-pick at twilight or apply biological *Bacillus thuringiensis* (Bt) spray.\n"
                f"- **Slugs & Snails:** Place shallow beer traps at soil level or sprinkle crushed eggshells around stems.\n\n"
                f"### 🐞 3. Beneficial Predator Allies\n"
                f"- Encourage ladybugs, lacewings, and hoverflies—they eat hundreds of aphids daily!"
            )
            suggested_follow_ups = [
                "What companion plants deter garden pests?",
                "How do I make a baking soda spray for fungal spots?",
                "Is neem oil safe for flowering plants?"
            ]

        # =========================================================================
        # 7. SUNLIGHT, CLIMATE & INDOOR CARE
        # =========================================================================
        elif any(term in q_lower for term in [
            "sun", "sunlight", "shade", "light", "temperature", "heat", "frost",
            "cold", "humidity", "indoor", "grow light", "scorched", "sunburn"
        ]):
            answer = (
                f"☀️ **Sunlight and climate control are vital for plant energy and immune defense!** Here is the breakdown for **{crop if has_scan else 'your plants'}**:\n\n"
                f"### 🌞 1. Sunlight Categories\n"
                f"- **Full Sun (6 to 8+ hours daily):** Essential for fruiting vegetables (Tomatoes, Peppers, Corn, Squash, Eggplants, Grapes).\n"
                f"- **Partial Sun / Dappled Light (3 to 6 hours):** Ideal for leafy greens (Spinach, Lettuce), herbs, and brassicas.\n"
                f"- **Bright Indirect Light:** Perfect for most indoor houseplants (avoids scorching delicate leaves).\n\n"
                f"### 🔥 2. Heatwave & Sunburn Protection\n"
                f"- When temperatures soar above **35°C (95°F)**, install a **30-40% shade cloth** over sensitive garden beds.\n"
                f"- White bleached patches on upper leaves indicate **Sunscald/Sunburn**—increase morning hydration.\n\n"
                f"### ❄️ 3. Cold & Frost Safeguards\n"
                f"- Cover plants with breathable frost cloth before nightfall if temperatures drop near 0°C (32°F).\n"
                f"- Mulch around the base to insulate soil roots."
            )
            suggested_follow_ups = [
                "How often should I water during hot summer days?",
                "Why are my plant leaves turning yellow?",
                "What is the best way to prune plants?"
            ]

        # =========================================================================
        # 8. PRUNING, TRIMMING & TOOL HYGIENE
        # =========================================================================
        elif any(term in q_lower for term in [
            "prune", "pruning", "trim", "trimming", "cut", "sanitize",
            "sterilize", "shears", "scissors", "sucker", "disinfect"
        ]):
            answer = (
                f"✂️ **Pruning is surgical plant care—done right, it stops disease dead in its tracks!** Here is how to prune **{crop if has_scan else 'your plants'}** like a pro:\n\n"
                f"### 🧼 1. Shears Sanitation (Crucial Step)\n"
                f"- Always dip or wipe pruning shears in **70% isopropyl alcohol** or a 10% bleach solution between every single plant.\n"
                f"- This stops microscopic fungal spores and bacteria from hitchhiking to healthy branches.\n\n"
                f"### 🌿 2. What to Cut First\n"
                f"- **Bottom 12 inches (30 cm) Canopy:** Strip off all leaves touching the ground to eliminate soil-splash contagion.\n"
                f"- **The 3 D's:** Immediately prune anything that is **Dead, Damaged, or Diseased**.\n"
                f"- **Crossed & Crowded Stems:** Thin the inner center to let sunlight and fresh breezes circulate through the foliage.\n\n"
                f"### 🗑️ 3. Safe Disposal Rules\n"
                f"- **NEVER compost diseased foliage** (home compost piles rarely get hot enough to destroy pathogens).\n"
                f"- Bag infected clippings in sealed plastic trash bags or burn where permitted."
            )
            suggested_follow_ups = [
                "How do I make a homemade organic spray?",
                "Will this disease spread to other garden plants?",
                "What chemical fungicide is best for plants?"
            ]

        # =========================================================================
        # 9. ORGANIC REMEDIES & HOMEMADE SPRAYS
        # =========================================================================
        elif any(term in q_lower for term in [
            "organic", "home remedy", "natural", "baking soda", "neem",
            "spray at home", "diy", "milk", "tea", "garlic", "peroxide"
        ]):
            answer = (
                f"🌿 **Let's treat this naturally and safely!** Here is a proven organic recipe arsenal for **{disease_name if has_scan else 'plant diseases'}** on **{crop}**:\n\n"
                f"### 🥣 1. Master Baking Soda Anti-Fungal Foliar Spray\n"
                f"- **Ingredients:**\n"
                f"  • 1 tablespoon Baking Soda (or Potassium Bicarbonate for gentler action)\n"
                f"  • 1 teaspoon cold-pressed pure Neem Oil (or vegetable horticultural oil)\n"
                f"  • 1/2 teaspoon liquid Castile Soap (acts as an organic emulsifier/sticker)\n"
                f"  • 1 gallon (3.8 Liters) lukewarm water\n"
                f"- **How to Apply:** Spray both **top and undersides of leaves** early in the morning. Reapply every 5 to 7 days or after rainfall.\n\n"
                f"### 🥛 2. Milk & Water Spray (Superb for Powdery Mildew)\n"
                f"- Mix **1 part milk with 9 parts water**. When exposed to morning sunlight, milk proteins produce natural antiseptic compounds that eliminate mildew spores.\n\n"
                f"### 🛡️ 3. Bio-Fungicide Support\n"
                f"- {organic_sol}\n"
                f"- Sprays with beneficial bacteria (*Bacillus subtilis*) or mycorrhizal inoculants crowd out pathogens."
            )
            suggested_follow_ups = [
                f"What chemical fungicides are strongest against {disease_name}?",
                "Can I safely eat vegetables from this plant?",
                "How does high humidity accelerate plant disease?"
            ]

        # =========================================================================
        # 10. CHEMICAL TREATMENTS & FUNGICIDE ROTATION
        # =========================================================================
        elif any(term in q_lower for term in [
            "chemical", "fungicide", "bactericide", "mancozeb", "copper",
            "chlorothalonil", "medicine", "synthetic", "spray schedule", "dosage", "frac"
        ]):
            answer = (
                f"🧪 **Here is your professional chemical treatment and rotation strategy for {disease_name if has_scan else 'crop diseases'}:**\n\n"
                f"### 1. Recommended Active Ingredients\n"
                f"- **Contact Protectants (Multi-Site):** {chemical_sol if chemical_sol else 'Copper Octanoate / Copper Hydroxide or Chlorothalonil.'} Coat leaves before infection spreads.\n"
                f"- **Systemic Options (Curative):** Azoxystrobin, Difenoconazole, or Propiconazole (absorbed into leaf vascular tissue).\n\n"
                f"### 2. Application & FRAC Rotation Protocol\n"
                f"- Spray during calm, dry weather early in the morning so droplets dry evenly.\n"
                f"- **Rotate FRAC Codes:** Never use the same systemic chemical class more than 2 times consecutively to prevent fungal strains from developing resistance.\n"
                f"- Observe a **7 to 14 day interval** between spray treatments.\n\n"
                f"### 3. Personal Safety Advisory\n"
                f"- {caution_text}\n"
                f"- Always wear goggles, an N95 mask, and chemical-resistant nitrile gloves."
            )
            suggested_follow_ups = [
                "What is the difference between contact and systemic fungicides?",
                "How many days should I wait before harvesting after spraying?",
                "Can I alternate organic copper with bio-fungicides?"
            ]

        # =========================================================================
        # 11. EDIBILITY & HARVEST SAFETY
        # =========================================================================
        elif any(term in q_lower for term in [
            "eat", "edible", "safe to harvest", "consume", "poisonous",
            "toxic", "fruit", "harvest", "phi", "pre harvest", "wash"
        ]):
            if "Healthy" in disease_name:
                answer = (
                    f"🍅 **Wonderful news! Your harvest is 100% healthy and safe to eat!**\n\n"
                    f"Your **{crop}** foliage and fruits are in great condition. Simply wash under clean tap water as usual and enjoy your fresh, homegrown produce!"
                )
            else:
                answer = (
                    f"🍎 **Here is my straightforward agronomist food safety assessment for {crop} affected by {disease_name}:**\n\n"
                    f"### 1. Unblemished Fruits & Vegetables (SAFE TO EAT ✅)\n"
                    f"- Any fruit that is firm, smooth, and free of lesions, sunken black rot, or mold is **completely safe to eat** after washing thoroughly under clean water and peeling if desired.\n\n"
                    f"### 2. Spotted or Blighted Fruits (DISCARD ❌)\n"
                    f"- Do not eat produce showing dark sunken lesions, foul odors, or fungal fuzz.\n"
                    f"- **Never can or preserve diseased fruit**, as fungal/bacterial breakdown alters acidity levels and compromises preservation safety.\n\n"
                    f"### 3. Pre-Harvest Interval (PHI) Caution\n"
                    f"- If you applied synthetic chemical sprays, strictly observe the **PHI wait period** (typically 3 to 14 days listed on the product container) before harvesting."
                )
            suggested_follow_ups = [
                f"What is the best way to wash harvested {crop}?",
                f"How do I prevent {disease_name} from reaching the fruits?",
                "What organic spray has zero days pre-harvest interval?"
            ]

        # =========================================================================
        # 12. CONTAGION, QUARANTINE & CROSS-INFECTION
        # =========================================================================
        elif any(term in q_lower for term in [
            "spread", "contagious", "neighbor", "other plants", "potatoes",
            "tomatoes", "quarantine", "isolate", "cross infection", "distance"
        ]):
            answer = (
                f"🛑 **Let's protect your garden from spreading!** Here is what you need to know about **{disease_name}** on **{crop}**:\n\n"
                f"- **Contagion Level:** **{severity}**\n"
                f"- **Transmission Pathways:** Spores travel via **wind gusts, splashing rainwater/sprinklers, contaminated gardening gloves, and dirty shears**.\n\n"
                f"### 🛡️ Immediate Quarantine & Containment Steps:\n"
                f"1. **Isolate Potted Plants:** Move infected containers at least **2 to 3 meters (6 to 10 feet)** away from healthy crops.\n"
                f"2. **Stop Overhead Irrigation:** Water directly at the soil line with a drip system or watering can.\n"
                f"3. **Watch Family Sibling Crops:** Plants in the same botanical family (e.g. Solanaceae: Tomatoes, Potatoes, Eggplants, Peppers) readily share pathogens like Early Blight and Late Blight.\n"
                f"4. **Sterilize Hands & Tools:** Wipe pruning shears with rubbing alcohol immediately after pruning infected foliage."
            )
            suggested_follow_ups = [
                "How do I properly sterilize garden soil after disease?",
                "What companion plants deter fungal and bacterial pathogens?",
                f"What is the complete prevention checklist for {crop}?"
            ]

        # =========================================================================
        # 13. COMPANION PLANTING & CROP ROTATION
        # =========================================================================
        elif any(term in q_lower for term in [
            "companion", "rotate", "rotation", "marigold", "basil",
            "garlic", "companion planting", "crop rotation", "next year"
        ]):
            answer = (
                f"🌼 **Companion planting and smart crop rotation are nature's best defense system!** Here is the agronomist strategy for **{crop}**:\n\n"
                f"### 🌸 1. Top Companion Plants\n"
                f"- **French Marigolds:** Excrete natural nematicides from roots and repel whiteflies, aphids, and beetles.\n"
                f"- **Sweet Basil:** Boosts vigor, attracts pollinators, and deters thrips and tomato hornworms.\n"
                f"- **Garlic & Chives:** Emit natural sulfur compounds that discourage fungal spore growth.\n\n"
                f"### 🔄 2. The 3-Year Crop Rotation Rule\n"
                f"- Never plant members of the same botanical family in the exact same garden bed for 3 consecutive seasons.\n"
                f"- Rotate nightshades (tomatoes/potatoes) with **legumes (beans/peas)** to replenish nitrogen, followed by **brassicas (cabbage/broccoli)**."
            )
            suggested_follow_ups = [
                "How do I sterilize soil between planting seasons?",
                "What are the best companion plants for tomatoes?",
                "What organic spray can I prepare at home?"
            ]

        # =========================================================================
        # 14. DEFAULT / GENERAL BOTANICAL DIAGNOSIS
        # =========================================================================
        else:
            answer = (
                f"🩺 **Here is my botanical diagnosis and care prescription for you:**\n\n"
                f"**Crop & Condition:** {crop} • **{disease_name}**\n"
                f"**Pathology Classification:** {matched_info.get('category', 'Condition')} (Severity: **{severity}**)\n\n"
                f"### 🔬 What Is Happening?\n"
                f"{cause_text}\n\n"
                f"### 🌿 What You Should Do First:\n"
                f"1. **Organic Response:** {organic_sol}\n"
                f"2. **Chemical Option:** {chemical_sol}\n"
                f"3. **Hygiene Action:** {prevention_list[0] if prevention_list else 'Ensure optimal air circulation and prune damaged foliage.'}\n\n"
                f"💬 *Feel free to ask me for a DIY spray recipe, watering schedule, edibility safety check, or step-by-step quarantine guide!*"
            )
            suggested_follow_ups = matched_info.get("recommended_questions", [
                "What questions can I ask about a plant?",
                f"What organic spray can I prepare for {disease_name}?",
                "Why are my plant leaves turning yellow?",
                "Is this disease contagious to my other garden plants?"
            ])

        return {
            "answer": answer,
            "disease_context": disease_name,
            "crop": crop,
            "severity": severity,
            "suggested_follow_ups": suggested_follow_ups
        }


_agent_instance = None

def get_plant_agent() -> PlantHealthAgent:
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = PlantHealthAgent()
    return _agent_instance


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    agent = PlantHealthAgent()
    
    print("--- Test 1: What can I ask? ---")
    res1 = agent.generate_response("what are the question we ask about a plant")
    print(res1["answer"][:200], "...\nFollow-ups:", res1["suggested_follow_ups"])
    
    print("\n--- Test 2: Yellowing leaves ---")
    res2 = agent.generate_response("Why are my leaves turning yellow and curling?")
    print(res2["answer"][:200], "...\n")
    
    print("\n--- Test 3: Water guide ---")
    res3 = agent.generate_response("How often should I water my tomato plants?")
    print(res3["answer"][:200], "...\n")
