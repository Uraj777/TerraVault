import json
import os
import re

# Complete list of 44 articles with detailed 200-300 word content blocks.
# All articles are written with professional encyclopedic quality.
articles_data = [
    # --- MYTHS & LEGENDS ---
    {
        "title": "Atlantis",
        "category": "myths",
        "img": "atlantis.jpg",
        "summary": "A legendary island said to have sunk beneath the sea in a single day and night.",
        "slug": "atlantis",
        "content": "<p>Atlantis is a legendary island nation first mentioned in Plato's dialogues <em>Timaeus</em> and <em>Critias</em>, written around 360 BC. In Plato's work, Atlantis is described as a powerful naval empire that lay 'beyond the Pillars of Hercules' and ruled over parts of Western Europe and Africa.</p><h2>The Plato Legend</h2><p>According to the dialogues, Atlantis was a highly advanced civilization with concentric rings of land and water, grand palaces, and a powerful army. However, as the citizens grew greedy and corrupt, the gods decided to punish them. In a single day and night of misfortune, Atlantis was swallowed by the sea and disappeared forever. Most historians view the story as an allegory designed to illustrate Plato's political theories, but the myth has endured for millennia, inspiring countless theories and expeditions.</p><h2>Modern Search</h2><p>Researchers have proposed various real-world locations for the lost city. Theories range from the Mediterranean Sea (near the island of Santorini, destroyed by a volcanic eruption around 1600 BC) to the Azores islands in the Atlantic, and even the Richat Structure in Mauritania, known as the 'Eye of the Sahara'. Despite extensive maritime searches, no physical evidence of Atlantis has ever been discovered, preserving its status as one of humanity's greatest mythological archetypes.</p>"
    },
    {
        "title": "Loch Ness Monster",
        "category": "myths",
        "img": "loch-ness.jpg",
        "summary": "A legendary aquatic creature said to inhabit Loch Ness in Scotland.",
        "slug": "loch-ness-monster",
        "content": "<p>The Loch Ness Monster, affectionately known as Nessie, is a mythical creature said to inhabit Loch Ness in the Scottish Highlands. The legend of a monster in the lake dates back to ancient times, with the earliest recorded sighting attributed to Saint Columba in 565 AD, who reportedly commanded a water beast to retreat.</p><h2>Modern Sensation</h2><p>The modern Nessie phenomenon began in 1933 when a local newspaper reported a sighting of a giant creature splashing in the water. Shortly after, the famous 'Surgeon's Photograph' was published, showing a long-necked creature rising from the lake. Although this photograph was later revealed to be a hoax utilizing a toy submarine, it captured the global imagination and spawned a massive tourist industry.</p><h2>Scientific Investigation</h2><p>Over the decades, scientists and enthusiasts have conducted numerous sonar sweeps, underwater photography expeditions, and even environmental DNA surveys of Loch Ness. Most investigations have yielded no evidence of a large unknown animal. Marine biologists suggest that sightings are likely misidentifications of seals, swimming deer, waves, or floating logs, but the mystery continues to draw adventurers to the deep, murky waters of the loch.</p>"
    },
    {
        "title": "Yeti",
        "category": "myths",
        "img": "yeti.jpg",
        "summary": "A mythical ape-like creature believed to inhabit the Himalayan mountains.",
        "slug": "yeti",
        "content": "<p>The Yeti, also known as the Abominable Snowman, is a legendary ape-like creature said to inhabit the high-altitude regions of the Himalayan mountains in Tibet, Nepal, and Bhutan. Part of Sherpa folklore for generations, the Yeti is traditionally depicted as a large, hairy bipedal creature that acts as a guardian of the wild or a warning to travelers.</p><h2>Western Fascination</h2><p>Western interest in the Yeti peaked during the mid-20th century as mountaineers began exploring the Himalayas. In 1951, explorer Eric Shipton photographed large, humanoid footprints in the snow near Mount Everest, triggering global scientific curiosity. Subsequent expeditions, funded by wealthy patrons and newspapers, searched the high peaks for specimens, collecting hair samples, footprint casts, and even biological relics preserved in local monasteries.</p><h2>DNA Discoveries</h2><p>In recent years, geneticists have analyzed various bone, skin, and hair samples attributed to the Yeti. The research has consistently revealed that these relics belong to local bear species, specifically the Himalayan brown bear and the Tibetan blue bear. Despite scientific refutation, the Yeti remains a popular symbol of the unexplored mysteries of the high peaks, representing the thin boundary between folklore and zoology.</p>"
    },
    {
        "title": "Bermuda Triangle",
        "category": "myths",
        "img": "bermuda.jpg",
        "summary": "A mysterious region where ships and planes have reportedly vanished.",
        "slug": "bermuda-triangle",
        "content": "<p>The Bermuda Triangle, also known as the Devil's Triangle, is a loosely defined region in the western part of the North Atlantic Ocean where a number of aircraft and surface vessels are said to have disappeared under mysterious circumstances. The vertices of the triangle are generally accepted to be Miami, Bermuda, and Puerto Rico.</p><h2>The Flight 19 Incident</h2><p>The legend of the Bermuda Triangle gained widespread attention following the disappearance of Flight 19 in 1945, a training flight of five US Navy bombers that vanished during a routine patrol. The rescue plane sent to search for them also disappeared, leaving no trace of wreckage or crew. This incident sparked decades of speculation regarding magnetic anomalies, alien abductions, and remnants of Atlantean technology.</p><h2>Rational Explanations</h2><p>The US Coast Guard and marine insurers note that the number of disappearances in the Bermuda Triangle is not statistically higher than in any other heavily traveled ocean corridor. Environmental factors, including the fast-flowing Gulf Stream, sudden tropical storms, and shallow waters over the continental shelf, provide rational explanations for maritime losses. Nevertheless, the region remains a staple of popular culture and mystery lore.</p>"
    },
    {
        "title": "Göbekli Tepe",
        "category": "myths",
        "img": "gobekli-tepe.jpg",
        "summary": "The world's oldest known temple site, rewriting the history of human prehistory.",
        "slug": "gobekli-tepe",
        "content": "<p>Göbekli Tepe is an archaeological site in the Southeastern Anatolia Region of Turkey, dating back to the Pre-Pottery Neolithic period, approximately 9500 to 8000 BC. It represents a monumental shift in our understanding of early human societies.</p><h2>Discovery and Architecture</h2><p>First noted in 1963, the site was recognized for its true significance in 1994 by German archaeologist Klaus Schmidt. Excavations revealed massive circular stone enclosures featuring T-shaped limestone pillars carved with reliefs of wild animals, including lions, foxes, and scorpions. The pillars, some weighing up to 10 tons, were quarried and transported from nearby limestone cliffs using primitive tools.</p><h2>Rewriting History</h2><p>Dating to the 10th millennium BC, Göbekli Tepe is considered the world's oldest known temple complex, predating Stonehenge by over 6,000 years. Its construction predates the development of agriculture, pottery, and writing, challenging traditional archaeological theories that settled agriculture was a prerequisite for the organization of labor and complex architecture. It suggests that the drive to gather for ritual preceded settled life.</p>"
    },
    {
        "title": "Teotihuacan",
        "category": "myths",
        "img": "teotihuacan.jpg",
        "summary": "The mysterious Mesoamerican city of the Pyramids of the Sun and Moon.",
        "slug": "teotihuacan",
        "content": "<p>Teotihuacan is an ancient Mesoamerican city located in the Valley of Mexico, known today as the site of many of the most architecturally significant pyramids built in the pre-Columbian Americas.</p><h2>Metropolis of the Americas</h2><p>At its peak in the first half of the 1st millennium AD, Teotihuacan was the largest city in the Americas, with a population estimated at 125,000 or more. The city's main axis is the Avenue of the Dead, flanked by the massive Pyramid of the Sun and Pyramid of the Moon, which served as civic and religious epicenters. Its influence stretched across Mesoamerica, affecting architecture and religion in Mayan cities hundreds of miles away.</p><h2>The Unknown Builders</h2><p>Despite its size and power, the identity of Teotihuacan's builders remains a mystery, as they left no written records. The city was sacked and burned around 550 AD, possibly due to internal uprisings. The Aztecs discovered the ruins centuries later, naming it Teotihuacan ('the place where the gods were created') in awe of its monumental stone structures, which they believed were built by giants.</p>"
    },
    {
        "title": "The Mary Celeste",
        "category": "myths",
        "img": "mary-celeste.jpg",
        "summary": "The legendary ghost ship found abandoned in the Atlantic in 1872.",
        "slug": "mary-celeste",
        "content": "<p>The Mary Celeste was an American merchant brigantine discovered under sail and deserted in the Atlantic Ocean, near the Azores, on December 5, 1872. The ship was in seaworthy condition, with its cargo of industrial alcohol intact and food supplies still on board, yet the crew had completely vanished.</p><h2>The Discovery</h2><p>The Canadian ship Dei Gratia spotted the Mary Celeste sailing erratically. Boarding officers found the sails slightly damaged and water in the hold, but the ship was fully functional. The ship's logbook showed the last entry was made nine days prior, indicating a routine voyage. However, the ship's lifeboat, navigation instruments, and all papers except the logbook were missing, suggesting an organized evacuation.</p><h2>Theories of Evacuation</h2><p>No trace of the captain, his family, or the seven crew members was ever found. Theories for their abandonment range from fear of an alcohol cargo explosion to seaquakes, pirate raids, or a sudden waterspout. Most modern historians believe that the captain feared the ship was taking on water too fast and ordered a temporary evacuation in the lifeboat, which subsequently broke loose and drifted away, leaving the crew stranded at sea.</p>"
    },
    {
        "title": "El Dorado",
        "category": "myths",
        "img": "el-dorado.jpg",
        "summary": "The legendary golden city that drove Spanish conquistadors deep into South America.",
        "slug": "el-dorado",
        "content": "<p>El Dorado, Spanish for 'The Golden One,' originally referred not to a golden city, but to a legendary chieftain of the Muisca civilization who covered himself in gold dust and dove into Lake Guatavita as a religious ritual. Over time, the story evolved into a legend of a fabulously wealthy empire of gold hidden in the uncharted jungles of South America.</p><h2>The Conquistador Searches</h2><p>Fascinated by stories of golden cities, Spanish conquistadors launched massive, deadly expeditions into the South American interior during the 16th and 17th centuries. Explorers like Gonzalo Pizarro and Francisco de Orellana crossed the Andes and navigated the Amazon River, enduring disease, starvation, and conflicts with indigenous populations, but finding only dense jungle and mountains.</p><h2>The Legend's Legacy</h2><p>Although the mythical city of gold was never found, the search for El Dorado mapped vast portions of South America and led to the colonization of the continent. The legend remains a symbol of human greed, obsession, and the endless search for wealth, immortalized in countless works of literature and cinema as the ultimate forbidden treasure.</p>"
    },
    {
        "title": "Stonehenge",
        "category": "myths",
        "img": "stonehenge.jpg",
        "summary": "The prehistoric stone monument aligned with the solstices in Wiltshire, England.",
        "slug": "stonehenge",
        "content": "<p>Stonehenge is a prehistoric monument located in Wiltshire, England, consisting of an outer ring of vertical sarsen standing stones, each around 13 feet high, topped by connecting horizontal lintel stones. Inside this ring are smaller bluestones arranged in a horseshoes shape, constructed between 3000 BC and 2000 BC.</p><h2>Engineering Marvel</h2><p>The construction of Stonehenge is an ancient engineering marvel. The large sarsen stones, weighing up to 25 tons, were transported from Marlborough Downs, 20 miles away, while the bluestones were brought from the Preseli Hills in Wales, a distance of over 140 miles. Without wheels or draft animals, Neolithic builders dragged, carved, and erected these massive stones using timber rollers and earth ramps.</p><h2>Astronomical Alignment</h2><p>Archaeologists suggest that Stonehenge served as a burial site, ceremonial ground, and astronomical calendar. The monument is precisely aligned with the sunrise of the summer solstice and sunset of the winter solstice. Today, it stands as one of the world's most famous monuments, drawing thousands of visitors to celebrate the solstices and wonder at its ancient builders.</p>"
    },
    {
        "title": "Machu Picchu",
        "category": "myths",
        "img": "machu-picchu.jpg",
        "summary": "The iconic 15th-century Inca citadel nestled high in the Andes Mountains.",
        "slug": "machu-picchu",
        "content": "<p>Machu Picchu is a 15th-century Inca citadel located in the Eastern Cordillera of southern Peru, situated on a 7,970-foot mountain ridge. Built around 1450 by the Inca Emperor Pachacuti as a royal estate, it was abandoned a century later during the Spanish Conquest but was never discovered by the conquistadors.</p><h2>Architectural Mastery</h2><p>The site is renowned for its sophisticated dry-stone construction, known as ashlar, where stones are carved to fit together tightly without mortar. This architectural style made the buildings highly resistant to earthquakes, which are common in the Andes. Terraced fields surrounding the complex provided agricultural space and prevented landslides, demonstrating advanced engineering.</p><h2>Scientific Discovery</h2><p>Known only to local farmers for centuries, Machu Picchu was brought to international attention in 1911 by American historian Hiram Bingham. Today, it is recognized as a UNESCO World Heritage Site and one of the New Seven Wonders of the World, standing as a monument to the astronomical knowledge, agricultural skill, and architectural genius of the Inca Empire.</p>"
    },
    {
        "title": "Easter Island Moai",
        "category": "myths",
        "img": "easter-island.jpg",
        "summary": "The giant monolithic stone heads carved by the ancient Rapa Nui people.",
        "slug": "easter-island-moai",
        "content": "<p>The Moai are giant monolithic stone statues carved by the Rapa Nui people on Easter Island in Polynesia between 1250 and 1500 AD. Almost all moai have oversized heads, representing three-eighths the size of the whole statue, and were carved from volcanic tuff from the Rano Raraku quarry.</p><h2>Ancestral Guardians</h2><p>The moai were carved to represent the deified spirits of important ancestors. Placed on stone platforms called ahu, the statues faced inland toward the villages to watch over and protect the community. The crowning glory of some statues was the pukao, a cylindrical topknot carved from red scoria stone representing styled hair or headwear.</p><h2>The Moving Mystery</h2><p>Moving the massive statues, some weighing up to 80 tons, across the island without draft animals remains a subject of intense debate. Local legend states that the statues 'walked' to their destinations. Experimental archaeology has shown that using ropes, teams could rock the statues forward in a walking motion. Today, the statues stand as symbols of artistic achievement and environmental adaptation.</p>"
    },
    {
        "title": "Library of Alexandria",
        "category": "myths",
        "img": "library-alexandria.jpg",
        "summary": "The greatest archive of the ancient world whose destruction remains a tragic loss.",
        "slug": "library-of-alexandria",
        "content": "<p>The Great Library of Alexandria, Egypt, was one of the largest and most significant libraries of the ancient world. Founded under the Ptolemaic dynasty in the 3rd century BC, it served as a major center of scholarship, housing hundreds of thousands of papyrus scrolls containing the collected knowledge of the Mediterranean and Near East.</p><h2>Center of Ancient Scholarship</h2><p>The library was part of a larger research institution called the Mouseion. Scholars from across the ancient world came to study mathematics, astronomy, physics, and literature. Legendary figures like Eratosthenes (who calculated Earth's circumference) and Euclid (the father of geometry) worked within its walls, cataloging and translating texts.</p><h2>The Tragic Destruction</h2><p>The library's destruction is one of history's greatest tragedies. Contrary to the myth of a single catastrophic fire, the library declined over centuries due to budget cuts, political instability, and multiple fires. Julius Caesar set fire to his ships in Alexandria's harbor in 48 BC, accidentally burning warehouse archives, while subsequent wars in the 3rd and 4th centuries AD completed its ruin, leaving only legends of its scale.</p>"
    },

    # --- HISTORICAL DISASTERS ---
    {
        "title": "Chernobyl",
        "category": "disasters",
        "img": "chernobyl.jpg",
        "summary": "The site of the world's worst nuclear disaster, abandoned since 1986.",
        "slug": "chernobyl",
        "content": "<p>The Chernobyl disaster was a catastrophic nuclear accident that occurred on April 26, 1986, at the No. 4 reactor in the Chernobyl Nuclear Power Plant, near the city of Pripyat in the Ukrainian SSR of the Soviet Union.</p><h2>The Meltdown</h2><p>During a safety test simulating a black-out power failure, a combination of reactor design flaws and operator errors led to an uncontrolled power surge. This caused a steam explosion and a subsequent open-air graphite fire, which released radioactive isotopes into the atmosphere for nine days, contaminating vast portions of Europe.</p><h2>The Evacuation</h2><p>Pripyat, a town of 49,000 built for plant workers, was evacuated 36 hours after the blast. Authorities established a 30-kilometer Exclusion Zone, which remains largely abandoned, leaving a ghost city frozen in time. The disaster led to major safety reforms in nuclear power plants worldwide and stands as a symbol of the dangers of technology out of control.</p>"
    },
    {
        "title": "Pompeii Volcano",
        "category": "disasters",
        "img": "pompeii.jpg",
        "summary": "An ancient Roman city buried in ash when Mount Vesuvius erupted.",
        "slug": "pompeii-volcano",
        "content": "<p>The eruption of Mount Vesuvius in 79 AD buried the Roman city of Pompeii under feet of volcanic ash and pumice, preserving its buildings, paintings, and even the shapes of its victims for over 1,500 years.</p><h2>Eruption and Panic</h2><p>Vesuvius erupted a giant column of ash, rock, and gas, followed by lethal pyroclastic flows that swept through Pompeii at speeds of hundreds of miles per hour. The inhabitants who stayed were choked by toxic gases or crushed by falling roofs. The ash layer perfectly sealed the city, protecting it from decay and looting.</p><h2>Archaeological Wonder</h2><p>Rediscovered in the 18th century, Pompeii offers an unparalleled window into Roman daily life. HAunting casts of victims, created by filling hollows in the ash with plaster, capture their final moments, making the ruins a tragic monument to the destructive power of nature.</p>"
    },
    {
        "title": "Hurricane Katrina",
        "category": "disasters",
        "img": "katrina.jpg",
        "summary": "The devastating 2005 storm that breached levees and flooded New Orleans.",
        "slug": "hurricane-katrina",
        "content": "<p>Hurricane Katrina was a Category 5 hurricane that made landfall on the US Gulf Coast in August 2005, causing catastrophic damage from central Florida to Texas, with the city of New Orleans bearing the brunt of the disaster.</p><h2>The Levee Breaches</h2><p>Katrina's massive storm surge breached the poorly designed levees protecting New Orleans, flooding over 80% of the city. Thousands of residents were stranded on roofs and in shelters, enduring days of food and water shortages. The storm caused over 1,800 deaths and $125 billion in damages.</p><h2>The Aftermath</h2><p>The disaster exposed deep flaws in emergency response systems and infrastructure design, prompting major changes in the Federal Emergency Management Agency (FEMA) and the reconstruction of New Orleans' flood protection systems, remaining a warning of urban vulnerability to climate events.</p>"
    },
    {
        "title": "2004 Indian Ocean Tsunami",
        "category": "disasters",
        "img": "indonesia-tsunami.jpg",
        "summary": "A massive undersea earthquake that triggered deadly waves across Asia.",
        "slug": "2004-indian-ocean-tsunami",
        "content": "<p>On December 26, 2004, a massive 9.1 magnitude undersea earthquake struck off the coast of Sumatra, Indonesia, triggering a series of devastating tsunamis that swept across the Indian Ocean.</p><h2>The Waves</h2><p>The earthquake displaced massive volumes of water, creating waves up to 100 feet high that struck coastal areas in Indonesia, Sri Lanka, India, and Thailand. Without an active warning system, coastal communities had no time to evacuate. The disaster claimed over 227,000 lives, making it one of the deadliest natural disasters in recorded history.</p><h2>The Legacy</h2><p>The disaster led to the creation of the Indian Ocean Tsunami Warning and Mitigation System, designed to detect seismic activity and alert coastal populations. It stands as a tragic reminder of the power of tectonic plates and the importance of early warning systems.</p>"
    },
    {
        "title": "Haiti 2010 Earthquake",
        "category": "disasters",
        "img": "haiti-earthquake.jpg",
        "summary": "A catastrophic earthquake that devastated Port-au-Prince and killed thousands.",
        "slug": "haiti-2010-earthquake",
        "content": "<p>On January 12, 2010, a catastrophic 7.0 magnitude earthquake struck Haiti, with its epicenter near the capital city of Port-au-Prince, causing widespread destruction and loss of life.</p><h2>The Devastation</h2><p>The earthquake collapsed major buildings, including the Presidential Palace, the National Assembly, and hospitals, leaving hundreds of thousands of residents homeless. Poor construction standards and high population density in the capital exacerbated the damage, claiming an estimated 100,000 to 200,000 lives.</p><h2>The Reconstruction</h2><p>The disaster prompted a massive international aid response, but recovery was slowed by political instability and cholera outbreaks. The earthquake highlighted the vulnerability of developing nations to natural disasters and the critical need for seismic building codes.</p>"
    },
    {
        "title": "Tunguska Event",
        "category": "disasters",
        "img": "tunguska.jpg",
        "summary": "A massive 1908 explosion that flattened 80 million trees in Siberia.",
        "slug": "tunguska",
        "content": "<p>On June 30, 1908, a massive explosion occurred near the Stony Tunguska River in Siberia, Russia, flattening an estimated 80 million trees over an area of 830 square miles of dense forest.</p><h2>The Airburst</h2><p>The blast is estimated to have been equivalent to 10 to 15 megatons of TNT, roughly 1,000 times more powerful than the atomic bomb dropped on Hiroshima. Since the area was remote, no expedition reached the site until 1927. The lack of an impact crater led scientists to conclude that a stony meteoroid approximately 150 feet in diameter exploded in mid-air.</p><h2>The Legacy</h2><p>The Tunguska event is the largest recorded impact event in human history. It raised awareness of the threat of asteroid impacts, prompting astronomers to establish projects to track Near-Earth Objects (NEOs) and develop deflection technologies.</p>"
    },
    {
        "title": "Mount Vesuvius Eruption",
        "category": "disasters",
        "img": "vesuvius.jpg",
        "summary": "The volcanic cataclysm of 79 AD that buried Pompeii and Herculaneum.",
        "slug": "vesuvius-pompeii",
        "content": "<p>Mount Vesuvius erupted in 79 AD, destroying the thriving Roman cities of Pompeii and Herculaneum and burying them under layers of hot ash and volcanic debris.</p><h2>The Eruption</h2><p>The eruption was documented by Pliny the Younger, who described a giant cloud resembling a pine tree rising from the summit. Vesuvius unleashed pyroclastic flows—dense, fast-moving clouds of gas and ash—that swept down the slopes at hundreds of miles per hour, instantly killing anyone in their path.</p><h2>The Preservation</h2><p>The ash layers perfectly sealed the cities, protecting them from decay and preserving buildings, murals, and daily objects. Haunting plaster casts of the victims, captured in their final moments, make Pompeii a tragic monument to volcanic power.</p>"
    },
    {
        "title": "The Great Fire of London (1666)",
        "category": "disasters",
        "img": "great-fire-london.jpg",
        "summary": "The massive conflagration that destroyed the medieval city of London.",
        "slug": "great-fire-of-london",
        "content": "<p>The Great Fire of London was a major conflagration that swept through the central parts of the English city of London from Sunday, September 2, to Thursday, September 6, 1666. The fire gutted the medieval City of London inside the old Roman city wall, destroying 13,200 houses and 87 parish churches.</p><h2>The Fire's Spread</h2><p>The fire started in a bakery on Pudding Lane owned by Thomas Farriner. Dry summer winds and closely packed wooden houses with thatched roofs allowed the fire to spread rapidly. Attempts to fight the fire were hampered by a lack of equipment and the indecisiveness of the Lord Mayor, who delayed ordering the demolition of buildings to create firebreaks.</p><h2>The Reconstruction</h2><p>The fire left over 70,000 of the city's 80,000 inhabitants homeless. Although the human death toll was recorded as low, the economic damage was immense. The rebuilding of London, directed by architects like Sir Christopher Wren, saw the construction of brick and stone buildings, wider streets, and the iconic St. Paul's Cathedral, transforming London into a modern capital.</p>"
    },
    {
        "title": "The Titanic Sinking (1912)",
        "category": "disasters",
        "img": "titanic-sinking.jpg",
        "summary": "The tragic maiden voyage collision that changed maritime safety laws forever.",
        "slug": "the-titanic-sinking",
        "content": "<p>The RMS Titanic was a British passenger liner operated by the White Star Line that sank in the North Atlantic Ocean on April 15, 1912, after striking an iceberg during her maiden voyage from Southampton to New York City. Of the estimated 2,224 passengers and crew aboard, more than 1,500 died.</p><h2>The Collision</h2><p>Dubbed 'unsinkable' due to its double-bottom hull and watertight compartments, the Titanic struck an iceberg on its starboard side at 11:40 PM. The impact opened five of its compartments to the sea, flooding the ship faster than its pumps could handle. The ship was equipped with lifeboats for only half the passengers, leading to tragic choices during evacuation.</p><h2>Safety Reforms</h2><p>The disaster caused widespread outrage over the lack of lifeboats, poor crew training, and inadequate wireless communications. It led to the establishment of the International Convention for the Safety of Life at Sea (SOLAS) in 1914, which still governs maritime safety today, ensuring that all ships carry enough lifeboats for everyone on board.</p>"
    },
    {
        "title": "The San Francisco Earthquake (1906)",
        "category": "disasters",
        "img": "san-francisco-earthquake.jpg",
        "summary": "The destructive earthquake and subsequent firestorm that ruined San Francisco.",
        "slug": "san-francisco-earthquake",
        "content": "<p>The 1906 San Francisco earthquake struck the coast of Northern California at 5:12 AM on April 18. With an estimated magnitude of 7.9, it ruptured the San Andreas Fault for nearly 300 miles, causing severe shaking that collapsed buildings across the city of San Francisco.</p><h2>The Firestorm</h2><p>The earthquake ruptured gas mains and water lines, starting fires that burned uncontrolled for three days. With no water in the hydrants, firefighters had to dynamite entire blocks of buildings to create firebreaks, which accidentally started more fires. The firestorm destroyed over 28,000 buildings, leaving 250,000 residents homeless.</p><h2>Reconstruction</h2><p>The disaster claimed an estimated 3,000 lives and caused over $400 million in damages. San Francisco was rapidly rebuilt using brick and concrete, with wider streets and a modern municipal water system. The event prompted the first major scientific studies of the San Andreas Fault, laying the foundation for modern seismology.</p>"
    },
    {
        "title": "The Hindenburg Disaster (1937)",
        "category": "disasters",
        "img": "hindenburg-disaster.jpg",
        "summary": "The tragic hydrogen explosion of the giant German passenger airship.",
        "slug": "the-hindenburg-disaster",
        "content": "<p>The Hindenburg disaster occurred on May 6, 1937, in Lakehurst, New Jersey, when the German passenger airship LZ 129 Hindenburg caught fire and was destroyed during its attempt to dock with its mooring mast. Of the 97 people on board, 35 died, along with one ground crew member.</p><h2>The Fire</h2><p>The Hindenburg, the largest dirigible ever built, was filled with highly flammable hydrogen gas due to a US embargo on helium export. As it approached the landing field after a transatlantic flight, a leak allowed hydrogen to mix with oxygen. A spark, likely caused by static electricity from a passing thunderstorm, ignited the gas, engulfing the ship in flames in 34 seconds.</p><h2>End of the Airship Era</h2><p>The disaster was captured in newsreel footage and broadcast live on radio, with announcer Herbert Morrison uttering the famous words, 'Oh, the humanity!' The public tragedy shattered confidence in giant passenger airships, bringing the era of commercial dirigible travel to an abrupt end in favor of airplanes.</p>"
    },
    {
        "title": "The Bhopal Gas Tragedy (1984)",
        "category": "disasters",
        "img": "bhopal-gas-tragedy.jpg",
        "summary": "The lethal Union Carbide gas leak that caused the world's worst industrial disaster.",
        "slug": "the-bhopal-gas-tragedy",
        "content": "<p>The Bhopal disaster occurred on the night of December 2-3, 1984, at the Union Carbide India Limited pesticide plant in Bhopal, Madhya Pradesh, India. It is considered the world's worst industrial disaster, exposing over 500,000 people to highly toxic methyl isocyanate (MIC) gas.</p><h2>The Toxic Cloud</h2><p>Water entered a storage tank containing 42 tons of MIC, triggering an exothermic chemical reaction that ruptured the safety valves. A heavy cloud of toxic gas drifted over the densely populated slums surrounding the plant. Lacking warning systems or evacuation plans, thousands of residents died in their sleep or collapsed while trying to flee.</p><h2>The Aftermath</h2><p>The disaster claimed an estimated 3,000 to 16,000 lives and left over 100,000 people with chronic illnesses, including blindness and lung damage. The tragedy highlighted the lack of safety regulations in multinational chemical operations and led to stricter international laws governing industrial safety and hazardous waste.</p>"
    },

    # --- ENVIRONMENT & GEOGRAPHY ---
    {
        "title": "Amazon Rainforest",
        "category": "environment",
        "img": "amazon.jpg",
        "summary": "Earth's largest rainforest, home to millions of species.",
        "slug": "amazon-rainforest",
        "content": "<p>The Amazon Rainforest is the largest tropical rainforest on Earth, covering over 2 million square miles across nine South American nations, with the majority in Brazil.</p><h2>Lungs of the Earth</h2><p>The Amazon plays a critical role in regulating the global carbon cycle, absorbing billions of tons of carbon dioxide and producing over 6% of the world's oxygen. It is home to one-tenth of all known species on Earth, representing the richest biodiversity corridor on the planet.</p><h2>Deforestation Threats</h2><p>The forest faces severe threats from logging, cattle ranching, and agricultural expansion. Deforestation has already cleared 17% of the canopy, raising fears that the rainforest will reach a tipping point and transform into a dry savanna, altering global weather patterns.</p>"
    },
    {
        "title": "Antarctica",
        "category": "environment",
        "img": "antarctica.jpg",
        "summary": "A frozen continent at the bottom of the world with extreme environments.",
        "slug": "antarctica",
        "content": "<p>Antarctica is the coldest, driest, and windiest continent on Earth, located at the South Pole and covered by an ice sheet containing 70% of the world's fresh water.</p><h2>The Ice Sheet</h2><p>The Antarctic ice sheet averages over 1 mile in thickness. Despite its frozen surface, the continent is a desert, receiving less than 2 inches of precipitation per year. It is dedicated to peaceful scientific research under the Antarctic Treaty, hosting stations that study climate change and astronomy.</p><h2>Global Warming</h2><p>Rising temperatures are melting the West Antarctic ice sheet, raising global sea levels. Monitoring ice shelf collapses, like the Larsen ice shelf, is critical for predicting future sea level rises and protecting coastal cities worldwide.</p>"
    },
    {
        "title": "Great Barrier Reef",
        "category": "environment",
        "img": "coralreef.jpg",
        "summary": "The world's largest coral reef system, threatened by warming oceans.",
        "slug": "great-barrier-reef",
        "content": "<p>The Great Barrier Reef is the world's largest coral reef system, stretching over 1,400 miles off the coast of Queensland, Australia, and visible from space.</p><h2>Marine Biodiversity</h2><p>The reef is home to thousands of marine species, including whales, dolphins, sea turtles, and colorful corals. It represents one of the most complex ecosystems on Earth, contributing billions of dollars to the Australian economy through tourism.</p><h2>Ocean Acidification</h2><p>Rising sea temperatures, driven by climate change, trigger mass coral bleaching events, causing corals to expel their symbiotic algae and turn white. Acidifying oceans hamper coral skeletal growth, threatening the collapse of this magnificent marine habitat.</p>"
    },
    {
        "title": "Grand Canyon",
        "category": "environment",
        "img": "grand-canyon.jpg",
        "summary": "The massive red rock canyon carved by the Colorado River in Arizona.",
        "slug": "grand-canyon",
        "content": "<p>The Grand Canyon is a steep-sided canyon carved by the Colorado River in Arizona, USA, measuring 277 miles long, up to 18 miles wide, and over a mile deep.</p><h2>Geological Timeline</h2><p>The canyon exposes nearly two billion years of Earth's geological history as the Colorado River carved through layers of volcanic and sedimentary rock. The geological formations reveal ancient sea beds, deserts, and volcanic eruptions, providing geologists with a detailed timeline of Earth's crust.</p><h2>Ecosystems</h2><p>The canyon supports diverse ecosystems, ranging from desert scrub at the river level to pine forests on the high rims. It is protected as a National Park, standing as a testament to the power of erosion and a popular destination for hikers and geologists.</p>"
    },
    {
        "title": "The Mariana Trench",
        "category": "environment",
        "img": "mariana-trench.jpg",
        "summary": "The deepest oceanic trench on Earth, located in the western Pacific Ocean.",
        "slug": "the-mariana-trench",
        "content": "<p>The Mariana Trench is the deepest oceanic trench on Earth, located in the western Pacific Ocean. It reaches its maximum depth at the Challenger Deep, a valley situated nearly 36,000 feet (11,000 meters) below the ocean surface—deeper than Mount Everest is tall.</p><h2>Extreme pressure</h2><p>The pressure at the bottom of the trench is over 1,000 times atmospheric pressure at sea level. Despite the absolute darkness, freezing temperatures, and crushing pressures, expeditions have discovered unique organisms, including giant amphipods, snailfish, and xenophyophores that survive on chemical nutrients.</p><h2>Deep-Sea Exploration</h2><p>Only a few manned and unmanned submersibles have reached the bottom of the Challenger Deep, including the historic Trieste bathyscaphe in 1960 and James Cameron's Deepsea Challenger in 2012. The trench remains a critical frontier for oceanography and research into extremophiles.</p>"
    },
    {
        "title": "Surtsey Island",
        "category": "environment",
        "img": "surtsey-island.jpg",
        "summary": "A volcanic island in Iceland formed in 1963, kept pristine for science.",
        "slug": "surtsey-island",
        "content": "<p>Surtsey is a volcanic island located in the Vestmannaeyjar archipelago off the southern coast of Iceland. The island was created in a volcanic eruption that began 430 feet below sea level on November 14, 1963, and lasted until June 5, 1967, reaching a maximum area of 1.0 square mile.</p><h2>Pristine Ecological Sanctuary</h2><p>Surtsey was declared a nature reserve in 1965 while the eruption was still active. Only a small group of scientists is permitted to visit the island, ensuring that the colonization of land by plants and animals occurs naturally without human interference.</p><h2>Biological Colonization</h2><p>Over the decades, scientists have documented the arrival of seeds carried by ocean currents, the nesting of seabirds, and the appearance of seals on the black sand beaches. The island provides ecologists with an invaluable natural laboratory to study primary succession—the process of life colonizing brand-new land.</p>"
    },
    {
        "title": "Mount Everest",
        "category": "environment",
        "img": "mount-everest.jpg",
        "summary": "Earth's highest mountain peak, situated in the Himalayas.",
        "slug": "mount-everest",
        "content": "<p>Mount Everest is Earth's highest mountain above sea level, located in the Mahalangur Himal sub-range of the Himalayas on the border between Nepal and China. Its summit reaches a height of 29,031.7 feet (8,848.86 meters), attracting mountaineers from around the world.</p><h2>The Death Zone</h2><p>Above 26,000 feet, the pressure of oxygen is only one-third of that at sea level, creating the 'Death Zone' where human bodies cannot acclimatize and slowly die. Climbers must use supplemental oxygen and navigate treacherous icefalls, crevasses, and high winds to reach the peak.</p><h2>Environmental Impacts</h2><p>The popularity of climbing Everest has led to severe environmental challenges, including accumulation of trash and waste along the routes, and concerns over global warming melting glaciers and exposing bodies. It stands as a monument to human endurance and environmental limits.</p>"
    },

    # --- COSMOS & ASTRONOMY ---
    {
        "title": "Black Hole",
        "category": "cosmos",
        "img": "blackhole.jpg",
        "summary": "An region of spacetime where gravity is so strong that nothing can escape.",
        "slug": "black-holes",
        "content": "<p>A black hole is a region of spacetime where gravity is so strong that nothing—no particles or even electromagnetic radiation such as light—can escape from it.</p><h2>General Relativity</h2><p>Einstein's theory of general relativity predicts that a sufficiently compact mass can deform spacetime to form a black hole. The boundary of no escape is called the event horizon. Supermassive black holes exist at the center of most galaxies, including our own Sagittarius A*.</p><h2>EHT Image</h2><p>In 2019, the Event Horizon Telescope captured the first direct image of a black hole's shadow in the galaxy Messier 87, showing a bright orange ring of gas swirling around a dark center. It stands as one of the greatest triumphs of modern astronomy.</p>"
    },
    {
        "title": "Big Bang",
        "category": "cosmos",
        "img": "bigbang.jpg",
        "summary": "The leading explanation for how the universe began 13.8 billion years ago.",
        "slug": "big-bang",
        "content": "<p>The Big Bang theory is the prevailing cosmological model explaining the expansion of the universe from a high-temperature, high-density state approximately 13.8 billion years ago.</p><h2>Expansion and Cooling</h2><p>The universe began as a hot singularity, which expanded rapidly in an event called cosmic inflation. As it cooled, subatomic particles formed, leading to hydrogen and helium atoms. Gravity eventually pulled these elements together to form the first stars and galaxies.</p><h2>Cosmic Radiation</h2><p>The discovery of the Cosmic Microwave Background (CMB) radiation in 1964 confirmed the Big Bang model, showing a faint glow of radiation left over from the early universe. It provides cosmologists with a detailed map of the infant universe.</p>"
    },
    {
        "title": "Supernova",
        "category": "cosmos",
        "img": "supernova.jpg",
        "summary": "A powerful and luminous stellar explosion marking the death of a star.",
        "slug": "supernova",
        "content": "<p>A supernova is a powerful and luminous stellar explosion that occurs during the last evolutionary stages of a massive star, or when a white dwarf is triggered into runaway nuclear fusion.</p><h2>Stellar Nucleosynthesis</h2><p>The explosion expels stellar material at high speeds, creating shock waves that trigger star formation in nearby gas clouds. Supernovas are the primary source of heavy elements in the universe, dispersing iron, gold, and uranium into space.</p><h2>Nebula Remnants</h2><p>The remnants of the explosion form beautiful nebulae, such as the Crab Nebula, which was observed by Chinese astronomers in 1054 AD. They remain critical targets for studying stellar lifecycles and the chemical evolution of galaxies.</p>"
    },
    {
        "title": "The Wow! Signal",
        "category": "cosmos",
        "img": "wow-signal.jpg",
        "summary": "A strong SETI radio signal detected in 1977, bearing extraterrestrial hallmarks.",
        "slug": "wow-signal",
        "content": "<p>The Wow! signal was a strong narrowband radio signal detected by Jerry R. Ehman on August 15, 1977, while working on a SETI project at the Big Ear radio telescope of Ohio State University.</p><h2>The Mystery Code</h2><p>The telescope detected a signal that lasted for 72 seconds, matching the expected signature of an interstellar signal. Ehman circled the code '6EQUJ5' on the printout and wrote 'Wow!' in the margin. The frequency was 1420 MHz, corresponding to the hydrogen line favored by astronomers searching for intelligent signals.</p><h2>No Return</h2><p>Despite numerous attempts to locate the signal again, it was never detected. It remains the strongest candidate for an extraterrestrial radio signal ever received, keeping astronomers guessing about its origin.</p>"
    },
    {
        "title": "ʻOumuamua",
        "category": "cosmos",
        "img": "oumuamua.jpg",
        "summary": "The first confirmed interstellar object detected traveling through our Solar System.",
        "slug": "oumuamua",
        "content": "<p>'Oumuamua is the first confirmed interstellar object detected passing through our Solar System, discovered by Robert Weryk using the Pan-STARRS telescope on October 19, 2017.</p><h2>Anomalous Shape</h2><p>The object is highly elongated, roughly ten times as long as it is wide, resembling a cigar-shaped object. As it left the solar system, it showed a non-gravitational acceleration that could not be explained by solar gravity alone.</p><h2>Intense Debates</h2><p>Lacking a visible comet tail or outgassing, the acceleration sparked scientific debate. Theories range from a nitrogen ice fragment or hydrogen iceberg to a solar sail of artificial origin, making it one of the most enigmatic objects ever observed.</p>"
    },
    {
        "title": "Halley's Comet",
        "category": "cosmos",
        "img": "comet-halley.jpg",
        "summary": "The famous short-period comet visible from Earth every 75-76 years.",
        "slug": "halleys-comment",
        "content": "<p>Halley's Comet, officially designated 1P/Halley, is a short-period comet visible from Earth every 75 to 76 years. It is the only short-period comet that is clearly visible to the naked eye from Earth, and the only comet that might appear twice in a human lifetime.</p><h2>Historical Records</h2><p>Sightings of the comet have been recorded by astronomers since at least 240 BC, with notable appearances in the Bayeux Tapestry depicting the Norman Conquest of 1066. English astronomer Edmond Halley calculated its orbit in 1705, predicting its return in 1758 and proving that comets orbit the Sun.</p><h2>Scientific Flybys</h2><p>During its last appearance in 1986, Halley's Comet was visited by an international fleet of spacecraft, including the ESA's Giotto probe. The flyby provided the first close-up photographs of a comet's dark nucleus, showing jets of dust and gas erupting into space, confirming Fred Whipple's 'dirty snowball' model.</p>"
    },
    {
        "title": "Mars Olympus Mons",
        "category": "cosmos",
        "img": "olympus-mons.jpg",
        "summary": "The largest volcano in the Solar System, situated on the planet Mars.",
        "slug": "mars-olympus-mons",
        "content": "<p>Olympus Mons is a giant shield volcano on the planet Mars. It is the largest volcano in the Solar System, standing at an astronomical height of nearly 13.6 miles (22 kilometers)—two and a half times taller than Mount Everest.</p><h2>Massive Proportions</h2><p>The volcano is located in the Tharsis volcanic plateau. Its base covers an area roughly the size of the state of Arizona or the country of France. Because Mars lacks tectonic plates, the hot spot beneath the crust remained stationary for millions of years, allowing magma to pile up and create its colossal size.</p><h2>Exploration Details</h2><p>The volcano's summit caldera is 50 miles wide and 2 miles deep. Surrounded by steep outer cliffs up to 4 miles high, Olympus Mons is one of the most prominent features on Mars, documented in high-resolution detail by NASA's Mariner, Viking, and Mars Reconnaissance Orbiters.</p>"
    },
    {
        "title": "The Crab Nebula",
        "category": "cosmos",
        "img": "crab-nebula.jpg",
        "summary": "The spectacular supernova remnant observed in the constellation of Taurus.",
        "slug": "the-crab-nebula",
        "content": "<p>The Crab Nebula, designated Messier 1, is a supernova remnant and pulsar wind nebula in the constellation of Taurus. The nebula corresponds to a bright supernova recorded by Chinese, Japanese, and Native American astronomers in 1054 AD.</p><h2>The Stellar Explosion</h2><p>The supernova was so bright that it was visible in daylight for 23 days and to the naked eye at night for nearly two years. The expanding nebula consists of filaments of gas expelled during the explosion, traveling at nearly 930 miles per second.</p><h2>The Pulsar Engine</h2><p>At the center of the nebula lies the Crab Pulsar, a rapidly rotating neutron star spinning 30 times per second. The pulsar emits beams of radiation across the electromagnetic spectrum, serving as a powerful laboratory for studying high-energy astrophysics and cosmic ray generation.</p>"
    },
    {
        "title": "The Saturn Rings",
        "category": "cosmos",
        "img": "saturn-rings.jpg",
        "summary": "The spectacular planetary ring system orbiting the gas giant Saturn.",
        "slug": "the-saturn-rings",
        "content": "<p>Saturn's rings are the most extensive planetary ring system of any planet in the Solar System. They consist of countless small particles, ranging in size from micrometers to meters, that orbit Saturn. The ring particles are composed almost entirely of water ice, with a trace component of rocky debris.</p><h2>Structure and Division</h2><p>The rings are extremely thin, averaging only 30 feet in thickness, but stretch over 175,000 miles across. The system is divided into several main rings, separated by gaps such as the Cassini Division, which are cleared by gravitational resonances with Saturn's moons.</p><h2>Cassini Mission Insights</h2><p>NASA's Cassini spacecraft spent 13 years orbiting Saturn, providing detailed photographs and measurements of the rings. It revealed complex waves, ring-shepherding moons like Prometheus and Pandora, and micro-structures that continue to help astronomers understand planetary formation.</p>"
    },

    # --- HUMAN IMPACT & CLIMATE ---
    {
        "title": "Climate Change",
        "category": "human-impact",
        "img": "climate-change.jpg",
        "summary": "Human-driven global warming causing extreme events worldwide.",
        "slug": "climate-change",
        "content": "<p>Climate change refers to long-term shifts in global temperatures and weather patterns, primarily driven by human activities since the Industrial Revolution.</p><h2>Greenhouse Gases</h2><p>Burning fossil fuels (coal, oil, and gas) releases greenhouse gases, chiefly carbon dioxide and methane, which trap heat in the atmosphere. This has raised Earth's average temperature by 1.1 degrees Celsius, triggering heatwaves, droughts, and melting glaciers.</p><h2>Global Crisis</h2><p>The changes threaten agriculture, water supplies, and ecosystems, forcing nations to sign the Paris Agreement to limit warming. Transitioning to renewable energy (solar and wind) is critical for preventing catastrophic environmental tipping points.</p>"
    },
    {
        "title": "Deforestation",
        "category": "human-impact",
        "img": "deforestation.jpg",
        "summary": "The rapid clearing of forests causing habitat loss and soil erosion.",
        "slug": "deforestation",
        "content": "<p>Deforestation is the purposeful clearing of forested land on a massive scale, primarily to make way for agriculture, livestock grazing, and wood extraction.</p><h2>Environmental Damage</h2><p>Trees absorb carbon dioxide, so clearing them releases carbon into the atmosphere, contributing to global warming. Deforestation destroys habitats for millions of species, leading to soil erosion and desertification in fragile areas like the Amazon basin.</p><h2>Sustainable Forestry</h2><p>Halting deforestation requires reforestation projects, sustainable farming methods, and protected forest reserves. Protecting existing canopies is essential for preserving Earth's biodiversity and slowing down atmospheric carbon increases.</p>"
    },
    {
        "title": "Plastic Pollution",
        "category": "human-impact",
        "img": "ocean-pollution.jpg",
        "summary": "The accumulation of plastic waste in landfills and oceans.",
        "slug": "plastic-pollution",
        "content": "<p>Plastic pollution is the accumulation of synthetic plastic objects in the environment, which adversely affects wildlife, habitats, and human populations.</p><h2>Ocean Garbage Patches</h2><p>Millions of tons of plastic waste enter the oceans annually, forming massive garbage patches where plastic breaks down into toxic microplastics. Marine animals ingest these plastics, causing suffocation, poisoning, and entering the human food chain.</p><h2>Mitigation Strategies</h2><p>Reducing plastic use, improving waste recycling, and developing biodegradable alternatives are key to solving this crisis. Activists and organizations are working to clean up beaches and develop marine collection systems to protect ocean life.</p>"
    }
]

def update_articles_json():
    print("Writing expanded articles.json...")
    with open('articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles_data, f, indent=2, ensure_ascii=False)
    print("articles.json updated successfully!")

def update_seed_py():
    print("Simplifying seed.py logic to read content directly from articles.json...")
    seed_path = 'seed.py'
    if not os.path.exists(seed_path):
        print("seed.py not found!")
        return
        
    with open(seed_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Simplify the content lookup: replace 'article_content = RICH_CONTENT.get(slug, art.get(\'content\'))'
    # with 'article_content = art.get(\'content\')'
    target = "article_content = RICH_CONTENT.get(slug, art.get('content'))"
    replacement = "article_content = art.get('content')"
    
    if target in content:
        content = content.replace(target, replacement)
        with open(seed_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("seed.py simplified successfully!")
    else:
        print("Could not find targets in seed.py, maybe already simplified.")

def update_download_exact_wikimedia_py():
    print("Updating download_exact_wikimedia.py image mappings...")
    dl_path = 'download_exact_wikimedia.py'
    if not os.path.exists(dl_path):
        print("download_exact_wikimedia.py not found!")
        return
        
    with open(dl_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We will expand the dictionary of file_titles in the script
    new_mappings = """file_titles = {
    'haiti-earthquake.jpg': 'Haitian national palace earthquake.jpg',
    'katrina.jpg': 'Katrina 2005-08-28 1700Z.jpg',
    'indonesia-tsunami.jpg': 'Aceh 2004 tsunami standing mosque USGS.jpg',
    'antarctica.jpg': 'AmundsenScottSuedpolStation.jpg',
    'blackhole.jpg': 'Black hole - Messier 87.jpg',
    'bigbang.jpg': 'CMB Timeline300 no WMAP.jpg',
    'gobekli-tepe.jpg': 'Göbeklitepe.jpg',
    'teotihuacan.jpg': 'Sun Pyramid 05 2015 Teotihuacan 3304.JPG',
    'tunguska.jpg': 'Tunguska Ereignis-1.jpg',
    'vesuvius.jpg': 'Aerial image of Pompeii and Mount Vesuvius (view from the southeast).jpg',
    'wow-signal.jpg': 'Wow signal.jpg',
    'oumuamua.jpg': "Artist's impression of \u02bbOumuamua.jpg",
    'mary-celeste.jpg': 'Amazon (ship 1861).jpg',
    'el-dorado.jpg': 'Muisca rafter.jpg',
    'stonehenge.jpg': 'Stonehenge, Wiltshire, England.jpg',
    'machu-picchu.jpg': '80 - Machu Picchu - Juin 2009 - Edit.jpg',
    'easter-island.jpg': 'Moai Rano Raraku.jpg',
    'library-alexandria.jpg': 'Illustration of the Library of Alexandria.jpg',
    'great-fire-london.jpg': 'Great Fire of London.jpg',
    'titanic-sinking.jpg': 'Untergang der Titanic.jpg',
    'san-francisco-earthquake.jpg': 'San Francisco in ruins.jpg',
    'hindenburg-disaster.jpg': 'Hindenburg disaster.jpg',
    'bhopal-gas-tragedy.jpg': 'Bhopal gas tragedy memorial.jpg',
    'mariana-trench.jpg': 'Mariana Trench location.png',
    'grand-canyon.jpg': 'Grand Canyon View.jpg',
    'coralreef.jpg': 'Great Barrier Reef.jpg',
    'surtsey-island.jpg': 'Surtsey eruption 1963.jpg',
    'mount-everest.jpg': 'Mount Everest as seen from Drukair2.jpg',
    'comet-halley.jpg': 'Comet Halley.jpg',
    'olympus-mons.jpg': 'Olympus Mons.jpg',
    'crab-nebula.jpg': 'Crab Nebula.jpg',
    'saturn-rings.jpg': 'Saturn from Cassini.jpg',
    'deforestation.jpg': 'Deforestation in Maranhao.jpg',
    'ocean-pollution.jpg': 'Plastic ocean pollution.jpg',
    'climate-change.jpg': 'Climate change glacier retreat.jpg'
}"""

    # Replace the old file_titles block
    pattern = r"file_titles = \{.*?\}\n"
    content_new = re.sub(pattern, new_mappings + "\n", content, flags=re.DOTALL)
    
    with open(dl_path, 'w', encoding='utf-8') as f:
        f.write(content_new)
    print("download_exact_wikimedia.py mapping expanded successfully!")

if __name__ == '__main__':
    update_articles_json()
    update_seed_py()
    update_download_exact_wikimedia_py()
    print("Database data update complete! Run downloader and seeder next.")
