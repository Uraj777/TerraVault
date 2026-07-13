import os
import re
import json
from app import create_app
from app.extensions import db
from app.models.user import User, Profile, Role
from app.models.article import Article, Category, Tag, article_tags, ArticleVersion
from app.models.interaction import Media, Draft, Bookmark, ReadingHistory
from app.services.cms_service import CMSService
from app.utils.helpers import slugify

# Sample detailed content for articles to avoid placeholder text
RICH_CONTENT = {
    "atlantis": """
        <p>Atlantis is a legendary island nation first mentioned in Plato's dialogues <em>Timaeus</em> and <em>Critias</em>, written around 360 BC. In Plato's work, Atlantis is described as a powerful naval empire that lay "beyond the Pillars of Hercules" and ruled over parts of Western Europe and Africa.</p>
        
        <h2>The Plato Legend</h2>
        <p>According to the dialogues, Atlantis was a highly advanced civilization with concentric rings of land and water, grand palaces, and a powerful army. However, as the citizens grew greedy and corrupt, the gods decided to punish them. In a single day and night of misfortune, Atlantis was swallowed by the sea.</p>
        
        <h2>Modern Theories and Search</h2>
        <p>While most historians view Plato's story as an allegory designed to illustrate his political theories, many adventurers and researchers have searched for physical evidence of the city. Theories locate it in various places, including:</p>
        <ul>
            <li>The Mediterranean Sea (near the island of Santorini, destroyed by a volcanic eruption)</li>
            <li>The Atlantic Ocean (near the Azores islands)</li>
            <li>The Richat Structure in Mauritania (the "Eye of the Sahara")</li>
        </ul>
        
        <h2>Impact on Culture</h2>
        <p>Atlantis continues to inspire countless works of literature, cinema, and video games. It remains the ultimate archetype of a lost golden age and a cautionary tale about human hubris.</p>
    """,
    "chernobyl": """
        <p>The Chernobyl disaster was a catastrophic nuclear accident that occurred on April 26, 1986, at the No. 4 reactor in the Chernobyl Nuclear Power Plant, near the city of Pripyat in the north of the Ukrainian SSR in the Soviet Union.</p>
        
        <h2>The Eruption of Reactor 4</h2>
        <p>During a late-night safety test simulating a black-out power failure, a combination of reactor design flaws and operator errors led to an uncontrolled nuclear chain reaction. A massive steam explosion followed by an open-air graphite fire released radioactive isotopes into the atmosphere for nine days.</p>
        
        <h2>The Evacuation and Exclusion Zone</h2>
        <p>Pripyat was not immediately evacuated. It took nearly 36 hours before residents were told to leave their homes, expecting to return in a few days. The Soviet authorities eventually established a 30-kilometer (19 mi) radius Exclusion Zone around the plant, which remains largely uninhabited except for wildlife and a few elderly residents who returned.</p>
        
        <h2>Legacy and Lessons</h2>
        <p>The accident led to significant safety reforms across the nuclear power industry globally. The sarcophagus built over Reactor 4 has since been replaced by the New Safe Confinement structure. Today, Chernobyl is a symbol of nuclear danger and a unique wildlife reserve where nature has reclaimed abandoned concrete structures.</p>
    """,
    "pompeii-volcano": """
        <p>In the autumn of 79 AD, Mount Vesuvius erupted in one of the most famous and destructive volcanic events in European history. The eruption buried the Roman city of Pompeii under meters of ash, pumice, and stone, freezing a moment in history.</p>
        
        <h2>The Eruption Timeline</h2>
        <p>Vesuvius erupted with explosive violence, shooting a high column of ash and pumice into the stratosphere. Over the next 24 hours, lethal pyroclastic flows—fast-moving currents of superheated gas and rock—swept down the volcano's slopes, instantly killing anyone in their path and burying buildings.</p>
        
        <h2>Rediscovery and Excavations</h2>
        <p>Pompeii lay buried and forgotten for nearly 1,700 years until its accidental rediscovery in the 18th century. The ash layers excluded air and moisture, preserving buildings, paintings, everyday items, and even the hollow spaces left by decayed bodies, which archaeologists filled with plaster to create famous casts of the victims.</p>
        
        <h2>Tourism and Preservation</h2>
        <p>Today, Pompeii is a UNESCO World Heritage site and one of the world's most popular tourist destinations. It provides unparalleled insights into ancient Roman daily life, architecture, and art, while preservationists struggle to protect the exposed ruins from weather and crowds.</p>
    """,
    "amazon-rainforest": """
        <p>The Amazon Rainforest, also known in English as Amazonia, is a moist broadleaf tropical forest in the Amazon biome that covers most of the Amazon basin of South America. It represents over half of the planet's remaining rainforests and comprises the largest and most biodiverse tract of tropical rainforest in the world.</p>
        
        <h2>Unrivaled Biodiversity</h2>
        <p>The Amazon is home to an estimated 390 billion individual trees divided into 16,000 species. One in ten known species on Earth lives in the Amazon. This includes over 2,000 species of birds and mammals, and tens of thousands of plant species, many of which have medicinal value.</p>
        
        <h2>The Carbon Sink</h2>
        <p>Often referred to as the "lungs of the Earth," the Amazon plays a critical role in global climate regulation by absorbing vast amounts of carbon dioxide. However, climate change and human activities are pushing the forest toward a tipping point where it could shift into a dry savanna.</p>
    """,
    "deforestation": """
        <p>Deforestation is the purposeful clearing of forested land. Throughout history and into modern times, forests have been razed to make space for agriculture, animal grazing, and to obtain wood for fuel, manufacturing, and construction.</p>
        
        <h2>Major Drivers of Forest Loss</h2>
        <p>Today, the largest driver of deforestation is agriculture. Large-scale farming, beef cattle ranching, and soybean plantations require massive tracts of cleared land. Logging, road building, and urban expansion contribute further to the degradation of global forests.</p>
        
        <h2>Environmental Consequences</h2>
        <p>Deforestation has severe impacts on the planet's health, including:</p>
        <ul>
            <li><strong>Loss of Habitat:</strong> Seventy percent of Earth's land animals and plants live in forests, and many cannot survive the destruction of their homes.</li>
            <li><strong>Climate Change:</strong> Trees absorb greenhouse gases. Fewer trees mean more carbon dioxide entering the atmosphere, accelerating global warming.</li>
            <li><strong>Soil Erosion:</strong> Without tree roots to anchor soil, it washes away, leading to agricultural instability and landslides.</li>
        </ul>
    """,
    "climate-change": """
        <p>Climate change refers to long-term shifts in temperatures and weather patterns. Since the 1800s, human activities have been the main driver of climate change, primarily due to burning fossil fuels like coal, oil, and gas.</p>
        
        <h2>The Greenhouse Effect</h2>
        <p>Burning fossil fuels generates greenhouse gas emissions (like carbon dioxide and methane) that act like a blanket wrapped around the Earth, trapping the sun's heat and raising temperatures. Key emissions sources include transportation, industry, agriculture, and land clearing.</p>
        
        <h2>Global Consequences</h2>
        <p>The consequences of a warming planet are already visible and include:</p>
        <ul>
            <li>More intense droughts and water scarcity</li>
            <li>Severe wildfires and heatwaves</li>
            <li>Rising sea levels due to melting glaciers and polar ice sheets</li>
            <li>Catastrophic flooding and storms</li>
        </ul>
        
        <h2>Pathways to Action</h2>
        <p>Global agreements, such as the Paris Agreement, aim to limit warming to well below 2 degrees Celsius. This requires transitioning energy grids to renewable sources (wind, solar), improving energy efficiency, and restoring forest ecosystems.</p>
    """,
    "black-holes": """
        <p>A black hole is a region of spacetime where gravity is so strong that nothing—no particles or even electromagnetic radiation such as light—has enough energy to escape its gravitational pull. The theory of general relativity predicts that a sufficiently compact mass can deform spacetime to form a black hole.</p>
        
        <h2>Structure of a Black Hole</h2>
        <p>Black holes are characterized by several key boundaries:</p>
        <ul>
            <li><strong>Singularity:</strong> The point at the very center of a black hole where matter is crushed to infinite density and space and time cease to exist in their normal form.</li>
            <li><strong>Event Horizon:</strong> The boundary around the singularity. Once an object crosses the event horizon, it cannot escape, as the escape velocity exceeds the speed of light.</li>
            <li><strong>Accretion Disk:</strong> A superheated band of gas and dust spiraling around the black hole, emitting intense X-rays.</li>
        </ul>
        
        <h2>Discovery and Photography</h2>
        <p>For decades, black holes were theoretical concepts. However, in 2019, the Event Horizon Telescope project released the first-ever direct image of a black hole's shadow at the center of the Messier 87 galaxy, proving their physical existence beyond doubt.</p>
    """,
    "bermuda-triangle": """
        <p>The Bermuda Triangle, also known as the Devil's Triangle, is a loosely defined region in the western part of the North Atlantic Ocean where a number of aircraft and surface vessels are said to have disappeared under mysterious circumstances.</p>
        
        <h2>Famous Incidents</h2>
        <p>The legend of the Bermuda Triangle gained widespread attention following the disappearance of Flight 19 in 1945—a group of five US Navy torpedo bombers that vanished during a training flight. Over the years, other high-profile disappearances, such as the USS Cyclops in 1918, fueled the mystery.</p>
        
        <h2>Scientific Explanations</h2>
        <p>Most reputable sources, including the US Coast Guard and insurance underwriters, state that the Bermuda Triangle is not unusually dangerous. Scientific explanations for the disappearances include:</p>
        <ul>
            <li>Severe, sudden tropical storms and hurricanes</li>
            <li>The fast-moving Gulf Stream current, which can quickly erase evidence of wreckage</li>
            <li>Methane hydrate releases from the ocean floor, lowering water density and sinking ships</li>
            <li>Compass variations due to magnetic anomalies</li>
        </ul>
    """
}

def clean_articles_json():
    """Remove comments from articles.json and parse it."""
    json_path = 'articles.json'
    if not os.path.exists(json_path):
        return []
        
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Strip comments matching /* ... */
    cleaned = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"Error parsing articles.json: {e}")
        # Return fallback list if parsing fails
        return []

def seed_db():
    app = create_app()
    with app.app_context():
        print("Clearing existing database contents...")
        db.session.query(Bookmark).delete()
        db.session.query(ReadingHistory).delete()
        db.session.query(Draft).delete()
        db.session.query(Media).delete()
        db.session.execute(db.delete(article_tags))
        db.session.query(ArticleVersion).delete()
        db.session.query(Article).delete()
        db.session.query(Tag).delete()
        db.session.query(Category).delete()
        db.session.query(Profile).delete()
        db.session.query(User).delete()
        db.session.query(Role).delete()
        db.session.commit()
        
        print("Seeding Roles...")
        roles_data = [
            {'name': 'Guest', 'description': 'Unauthenticated visitor (read-only)'},
            {'name': 'User', 'description': 'Standard registered community member'},
            {'name': 'Moderator', 'description': 'Content reviewer and user monitor'},
            {'name': 'Admin', 'description': 'Global platform administrator'}
        ]
        
        roles_dict = {}
        for r_data in roles_data:
            role = Role(name=r_data['name'], description=r_data['description'])
            db.session.add(role)
            roles_dict[r_data['name']] = role
        db.session.commit()
        
        print("Seeding Users...")
        # Create Admin User
        admin = User(username='admin', email='admin@terravault.com', role_id=roles_dict['Admin'].id, is_verified=True, reputation=100)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.flush()
        
        # Create Profile
        admin_profile = Profile(user_id=admin.id, bio="TerraVault Global System Administrator.", location="Global")
        db.session.add(admin_profile)
        
        # Create Moderator User
        mod = User(username='moderator', email='mod@terravault.com', role_id=roles_dict['Moderator'].id, is_verified=True, reputation=50)
        mod.set_password('mod123')
        db.session.add(mod)
        db.session.flush()
        
        mod_profile = Profile(user_id=mod.id, bio="TerraVault Chief Editor & Content Reviewer.", location="London, UK")
        db.session.add(mod_profile)
        
        # Create Standard User
        user = User(username='explorer_bob', email='bob@gmail.com', role_id=roles_dict['User'].id, is_verified=True, reputation=15)
        user.set_password('bob123')
        db.session.add(user)
        db.session.flush()
        
        bob_profile = Profile(user_id=user.id, bio="Curious explorer fascinated by volcanic history and space anomalies.", location="New York, USA")
        db.session.add(bob_profile)
        
        db.session.commit()
        
        print("Seeding Categories...")
        categories_data = [
            {'slug': 'myths', 'name': 'Myths & Legends', 'description': 'Unraveling ancient legends, cryptids, and long-lost civilizations.'},
            {'slug': 'disasters', 'name': 'Historical Disasters', 'description': 'Revisiting cataclysms, nuclear catastrophes, and natural events that altered human courses.'},
            {'slug': 'environment', 'name': 'Environment & Geography', 'description': 'Exploring Earth\'s geographical anomalies, ecosystems, and environmental cycles.'},
            {'slug': 'cosmos', 'name': 'Cosmos & Astronomy', 'description': 'Venture into the stellar void: black holes, supernovas, and cosmological genesis.'},
            {'slug': 'human-impact', 'name': 'Human Impact & Climate', 'description': 'Investigating carbon footprints, global warming, deforested zones, and modern industry footprints.'}
        ]
        
        categories_dict = {}
        for c_data in categories_data:
            cat = Category(slug=c_data['slug'], name=c_data['name'], description=c_data['description'])
            db.session.add(cat)
            categories_dict[c_data['slug']] = cat
        db.session.commit()
        
        print("Loading and Seeding Articles...")
        raw_articles = clean_articles_json()
        
        for art in raw_articles:
            cat_slug = art.get('category')
            category = categories_dict.get(cat_slug)
            
            if not category:
                # Default to myths if category mapping fails
                category = categories_dict['myths']
                
            # Check for rich content override
            slug = art.get('slug')
            article_content = RICH_CONTENT.get(slug, art.get('content'))
            
            # Simple reference seeds
            ref_list = [
                "Encyclopaedia Britannica, Online Edition.",
                "National Geographic Historical Archives.",
                f"Scientific Reports on {art.get('title')} (2024)."
            ]
            ref_data = "\n".join(ref_list)
            
            # Generate article
            # Alternate authors between admin and mod
            author_id = admin.id if len(category.articles) % 2 == 0 else mod.id
            
            tags_list = [category.name.split()[0]]  # Seed one tag per category name
            
            CMSService.create_article(
                title=art.get('title'),
                summary=art.get('summary'),
                content=article_content,
                category_id=category.id,
                tags_list=tags_list,
                author_id=author_id,
                image_url=art.get('img'),
                is_published=True,
                is_featured=(art.get('slug') in ['atlantis', 'chernobyl', 'black-holes']), # Featured articles
                references_data=ref_data
            )
            
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_db()
