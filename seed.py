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
    """,
    "gobekli-tepe": """
        <p>Göbekli Tepe is an archaeological site in the Southeastern Anatolia Region of Turkey, dating back to the Pre-Pottery Neolithic period, approximately 9500 to 8000 BC.</p>
        
        <h2>Discovery and Excavation</h2>
        <p>First noted in a survey in 1963, the site was recognized for its true significance in 1994 by German archaeologist Klaus Schmidt. Excavations revealed massive circular stone enclosures featuring T-shaped limestone pillars carved with reliefs of wild animals.</p>
        
        <h2>Historical Significance</h2>
        <p>Dating to the 10th millennium BC, Göbekli Tepe is considered the world's oldest known megalithic structure. Its construction predates the development of agriculture, pottery, and metallurgy, challenging traditional theories that agriculture was a prerequisite for complex societies.</p>
    """,
    "teotihuacan": """
        <p>Teotihuacan is an ancient Mesoamerican city located in a sub-valley of the Valley of Mexico, known today as the site of many of the most architecturally significant Mesoamerican pyramids built in the pre-Columbian Americas.</p>
        
        <h2>Urban Planning and Pyramids</h2>
        <p>At its peak in the first half of the 1st millennium AD, Teotihuacan was the largest city in the pre-Columbian Americas, with a population estimated at 125,000 or more. The city's main axis is the Avenue of the Dead, flanked by the massive Pyramid of the Sun and Pyramid of the Moon.</p>
        
        <h2>Mysterious Collapse</h2>
        <p>The city was sacked and burned around 550 AD, and its builders left no written records. The Aztecs discovered the city centuries later, naming it Teotihuacan ("the place where the gods were created") in awe of its monumental architecture.</p>
    """,
    "tunguska": """
        <p>The Tunguska event was a massive explosion that occurred on June 30, 1908, near the Podkamennaya Tunguska River in Yeniseysk Governorate, Russia.</p>
        
        <h2>The Explosion and Damage</h2>
        <p>The explosion flattened an estimated 80 million trees over an area of 2,150 square kilometers (830 sq mi) of taiga forest. The energy of the blast is estimated to have been equivalent to 10 to 15 megatons of TNT—roughly 1,000 times more powerful than the atomic bomb dropped on Hiroshima.</p>
        
        <h2>Scientific Theories</h2>
        <p>Since the explosion occurred in a remote region, no expedition reached the site until Leonid Kulik's team in 1927. The lack of an impact crater led scientists to conclude that the blast was caused by the airburst of a stony meteoroid or comet approximately 50 to 100 meters in diameter.</p>
    """,
    "vesuvius-pompeii": """
        <p>The eruption of Mount Vesuvius in 79 AD was one of the most famous and catastrophic volcanic eruptions in European history, burying the Roman cities of Pompeii, Herculaneum, Oplontis, and Stabiae under meters of ash and pumice.</p>
        
        <h2>Cataclysm of 79 AD</h2>
        <p>The eruption was described in vivid detail by Pliny the Younger, who witnessed the event from across the Bay of Naples. Vesuvius erupted a giant cloud of ash, rock, and volcanic gases, followed by lethal pyroclastic flows that swept through the cities at hundreds of miles per hour.</p>
        
        <h2>Archaeological Discovery</h2>
        <p>Forgotten for over 1,500 years, the ruins of Pompeii were rediscovered in the 18th century. The ash layers perfectly preserved the buildings, wall paintings, and even hollow spaces left by decayed bodies, which archaeologists filled with plaster to create haunting casts of the victims.</p>
    """,
    "wow-signal": """
        <p>The Wow! signal was a strong narrowband radio signal detected by Jerry R. Ehman on August 15, 1977, while working on a SETI project at the Big Ear radio telescope of Ohio State University.</p>
        
        <h2>The "6EQUJ5" Code</h2>
        <p>The signal bore the expected hallmarks of non-terrestrial and non-solar system origin. Amazed at how closely the signal matched the expected signature of an interstellar signal, Ehman circled the anomaly on the computer printout and wrote the comment "Wow!" in the margin.</p>
        
        <h2>Unsolved Anomaly</h2>
        <p>Despite numerous attempts to locate the signal again, it was never detected. The frequency of the signal was 1420.405 MHz, which corresponds to the hydrogen line (the astronomical frequency favored by searchers for extraterrestrial intelligence).</p>
    """,
    "oumuamua": """
        <p>'Oumuamua is the first confirmed interstellar object detected passing through our Solar System, discovered by Robert Weryk using the Pan-STARRS telescope on October 19, 2017.</p>
        
        <h2>Anomalous Trajectory and Shape</h2>
        <p>'Oumuamua exhibited a non-gravitational acceleration as it left the solar system, which could not be explained by solar gravity alone. It is highly elongated, roughly ten times as long as it is wide, resembling a cigar-shaped object traveling at high speed.</p>
        
        <h2>Scientific Debates</h2>
        <p>The object's unusual shape, lack of visible outgassing (cometary tail), and subtle acceleration sparked intense scientific debate, with theories ranging from a hydrogen iceberg or nitrogen ice fragment to a solar sail of artificial origin.</p>
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
        print("Creating all database tables...")
        db.create_all()
        print("Clearing existing database contents...")
        
        # New community tables
        from app.models.community import (
            AnonymousVisitor, Community, Discussion, Comment, Vote, Report,
            NewsletterSubscriber, AuditLog, PageViewMetric, SearchMetric
        )
        db.session.query(Report).delete()
        db.session.query(Vote).delete()
        db.session.query(Comment).delete()
        db.session.query(Discussion).delete()
        db.session.query(Community).delete()
        db.session.query(AnonymousVisitor).delete()
        db.session.query(NewsletterSubscriber).delete()
        db.session.query(AuditLog).delete()
        db.session.query(PageViewMetric).delete()
        db.session.query(SearchMetric).delete()
        
        # Old tables
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
            {'name': 'Admin', 'description': 'Global platform administrator'},
            {'name': 'Guest', 'description': 'Visitor (read-only)'}
        ]
        
        roles_dict = {}
        for r_data in roles_data:
            role = Role(name=r_data['name'], description=r_data['description'])
            db.session.add(role)
            roles_dict[r_data['name']] = role
        db.session.commit()
        
        print("Seeding Admin User...")
        # Create Admin User
        admin = User(username='admin', email='admin@terravault.com', role_id=roles_dict['Admin'].id, is_verified=True, reputation=100)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.flush()
        
        # Create Profile
        admin_profile = Profile(user_id=admin.id, bio="TerraVault Global System Administrator.", location="Global")
        db.session.add(admin_profile)
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
                category = categories_dict['myths']
                
            ref_list = [
                "Encyclopaedia Britannica, Online Edition.",
                "National Geographic Historical Archives.",
                f"Scientific Reports on {art.get('title')} (2024)."
            ]
            ref_data = "\n".join(ref_list)
            
            # Author is always admin in new single-admin model
            author_id = admin.id
            tags_list = [category.name.split()[0]]
            
            CMSService.create_article(
                title=art.get('title'),
                summary=art.get('summary'),
                content=art.get('content'),
                category_id=category.id,
                tags_list=tags_list,
                author_id=author_id,
                image_url=art.get('img'),
                is_published=True,
                is_featured=(art.get('slug') in ['atlantis', 'chernobyl', 'black-holes']),
                references_data=ref_data
            )
            
        print("Seeding Communities...")
        communities_data = [
            {'name': 'History', 'slug': 'history', 'description': 'Discuss ancient records, historical milestones, and humanity\'s lineage.', 'icon': 'fa-monument'},
            {'name': 'Mythology', 'slug': 'mythology', 'description': 'Debate ancient legends, cryptids, folklore, and mythic civilizations.', 'icon': 'fa-dragon'},
            {'name': 'Disasters', 'slug': 'disasters', 'description': 'Revisit historical cataclysms, fires, volcanic eruptions, and nuclear accidents.', 'icon': 'fa-burst'},
            {'name': 'Environment', 'slug': 'environment', 'description': 'Share news and insights on Earth\'s ecosystems, climate change, and geographies.', 'icon': 'fa-leaf'},
            {'name': 'Cosmology', 'slug': 'cosmology', 'description': 'Explore stellar horizons: black holes, astronomical anomalies, and deep space.', 'icon': 'fa-meteor'},
            {'name': 'Archaeology', 'slug': 'archaeology', 'description': 'Discuss monuments, megaliths, ancient cities, and archaeological digs.', 'icon': 'fa-compass'}
        ]
        
        communities_dict = {}
        for comm in communities_data:
            c = Community(name=comm['name'], slug=comm['slug'], description=comm['description'], icon=comm['icon'])
            db.session.add(c)
            communities_dict[comm['slug']] = c
        db.session.commit()
        
        print("Seeding Mock Visitors and Discussions...")
        v1 = AnonymousVisitor(uuid="visitor-uuid-1", display_name="Anonymous Explorer #C3A9", avatar_color="hsl(210, 70%, 45%)")
        v2 = AnonymousVisitor(uuid="visitor-uuid-2", display_name="Anonymous Explorer #E5B2", avatar_color="hsl(120, 70%, 45%)")
        db.session.add_all([v1, v2])
        db.session.commit()
        
        # Seeding thread 1
        disc1 = Discussion(
            title="Did the Library of Alexandria have a sister branch?",
            content="We know the main library in the Bruchion district was destroyed, but did the Serapeum branch survive longer? If so, what scrolls did it hold?",
            community_id=communities_dict['history'].id,
            visitor_uuid=None,  # Posted by Editorial / Official
            status='published'
        )
        db.session.add(disc1)
        db.session.flush()
        
        # Seed comment on thread 1
        comment1 = Comment(
            content="According to historical accounts, the Serapeum did survive the initial fire and was used as a smaller repository, but it was destroyed later in 391 AD under the decree of Theophilus.",
            discussion_id=disc1.id,
            parent_id=None,
            visitor_uuid=v1.uuid
        )
        db.session.add(comment1)
        
        # Seeding thread 2
        disc2 = Discussion(
            title="The Mystery of 'Oumuamua's non-gravitational acceleration",
            content="Is there a final consensus on why 'Oumuamua accelerated as it left our system? The hydrogen iceberg theory seems plausible, but what do you think?",
            community_id=communities_dict['cosmology'].id,
            visitor_uuid=v2.uuid,
            status='published'
        )
        db.session.add(disc2)
        db.session.flush()
        
        # Comment and nested reply on thread 2
        comment2 = Comment(
            content="The solar radiation pressure explanation is still preferred by most astrophysicists, though it requires specific physical dimensions.",
            discussion_id=disc2.id,
            parent_id=None,
            visitor_uuid=None  # Posted by Editorial / Official
        )
        db.session.add(comment2)
        db.session.flush()
        
        reply2 = Comment(
            content="Exactly. It doesn't need to be an artificial light sail to accelerate from solar pressure, just thin and reflective.",
            discussion_id=disc2.id,
            parent_id=comment2.id,
            visitor_uuid=v1.uuid
        )
        db.session.add(reply2)
        
        # Seed some votes
        vote1 = Vote(visitor_uuid=v1.uuid, discussion_id=disc2.id, value=1)
        vote2 = Vote(visitor_uuid=v2.uuid, discussion_id=disc1.id, value=1)
        db.session.add_all([vote1, vote2])
        
        # Seed one report to show in the moderation queue
        report1 = Report(
            visitor_uuid=v1.uuid,
            discussion_id=disc2.id,
            reason="Misinformation",
            details="Some users are claiming it was definitely aliens.",
            status="pending"
        )
        db.session.add(report1)
        
        # Add Audit log
        audit = AuditLog(action="System Init", details="Database initialized and seeded with mock data.")
        db.session.add(audit)
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_db()

if __name__ == '__main__':
    seed_db()
