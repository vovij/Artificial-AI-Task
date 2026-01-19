"""System prompts for AI players and 460 secret object choices"""

PLAYER1_SYSTEM_PROMPT = """You are Player 1 in Twenty Questions. Your secret object is: '{secret_object}'.

RULES:
- ONLY answer 'yes', 'no', or 'maybe' if truly uncertain to yes/no questions
- If the player asks a non yes/no question (like "what is it?" or "why?"), respond: "Please ask a yes/no question"
- If the player guesses '{secret_object}' with MINOR typos (1-3 character mistakes like missing/extra/swapped letters), respond: "Yes! It's {secret_object}. You win!"
- Answer ONLY about {secret_object} specifically. Do not say "yes" to questions about different objects that seem similar.
- Do not help by saying "yes, but be specific" to wrong guesses - just say "no"
- Stay in character - you are answering questions about your secret object, nothing else"""


PLAYER2_SYSTEM_PROMPT = """You are Player 2 in Twenty Questions. Ask a CONCISE yes/no questions to guess the object.

STRATEGY:
- Questions 1-8: Start broad (alive? man-made? size? category?)
- Questions 9-15: Narrow down specific features
- Questions 16-20: Start making direct guesses - "Is it a [specific object]?"
- Try different categories if previous guesses fail

RULES:
- Keep questions short
- ONE question at a time
- Output ONLY the question itself, no numbering or labels
- After gathering enough information, make a direct guess. Keep in mind you have 20 questions until the game finishes"""

# 460 secret objects for ensured diversity. AI tended to pick the same secret objects if it was asked to generate one.
GAME_OBJECTS = [
    # Household items
    "toaster", "refrigerator", "microwave", "blender", "kettle", "iron", "vacuum", 
    "lamp", "mirror", "clock", "pillow", "blanket", "curtain", "rug", "mop",
    "broom", "scissors", "hammer", "screwdriver", "wrench", "drill", "ladder",
    "bucket", "sponge", "soap", "towel", "comb", "brush", "razor", "shampoo",
    
    # Kitchen items
    "fork", "spoon", "knife", "plate", "bowl", "cup", "mug", "glass", "pan",
    "pot", "spatula", "whisk", "grater", "peeler", "colander", "strainer",
    "teapot", "coffeepot", "thermos", "lunchbox", "chopsticks", "tongs",
    
    # Electronics
    "television", "radio", "telephone", "computer", "keyboard", "mouse", "monitor",
    "printer", "scanner", "speaker", "headphones", "camera", "flashlight", "battery",
    "calculator", "remote", "charger", "router", "modem", "tablet",
    
    # Furniture
    "chair", "table", "desk", "bed", "sofa", "couch", "bench", "stool", "cabinet",
    "shelf", "bookcase", "dresser", "wardrobe", "nightstand", "ottoman", "armchair",
    
    # Clothing & Accessories
    "shirt", "pants", "dress", "skirt", "jacket", "coat", "sweater", "hat", "cap",
    "scarf", "gloves", "socks", "shoes", "boots", "sandals", "belt", "tie", "watch",
    "sunglasses", "umbrella", "backpack", "purse", "wallet", "ring", "necklace",
    "bracelet", "earrings", "badge", "button",
    
    # Stationery & Office
    "pen", "pencil", "eraser", "ruler", "stapler", "paperclip", "notebook", "folder",
    "envelope", "stamp", "postcard", "calendar", "whiteboard", "marker", "crayon",
    "tape", "glue", "clipboard", "highlighter", "sharpener",
    
    # Sports & Recreation
    "ball", "bat", "racket", "frisbee", "skateboard", "bicycle", "helmet", "whistle",
    "trophy", "medal", "net", "goal", "hoop", "mitt", "glove", "paddle", "puck",
    "dumbbell", "barbell", "treadmill", "skates", "skis", "snowboard", "surfboard",
    
    # Musical Instruments
    "guitar", "piano", "violin", "drums", "flute", "trumpet", "saxophone", "harmonica",
    "accordion", "banjo", "cello", "clarinet", "harp", "trombone", "tuba", "tambourine",
    "xylophone", "maracas", "recorder", "ukulele",
    
    # Toys & Games
    "doll", "puzzle", "kite", "balloon", "yoyo", "dice", "chess", "checkers",
    "dominoes", "cards", "blocks", "lego", "marble", "spinner", "slinky",
    
    # Garden & Outdoor
    "shovel", "rake", "hose", "sprinkler", "lawnmower", "wheelbarrow", "fence",
    "gate", "flowerpot", "trowel", "shears", "watering", "seeds", "fountain",
    
    # Vehicles & Transportation
    "car", "truck", "bus", "train", "airplane", "helicopter", "boat", "ship",
    "motorcycle", "scooter", "ambulance", "firetruck", "taxi", "van", "submarine",
    "rocket", "yacht", "canoe", "kayak", "sailboat",
    
    # Tools & Hardware
    "saw", "chisel", "pliers", "axe", "nail", "screw", "bolt", "nut", "hinge",
    "lock", "key", "chain", "rope", "wire", "hook", "clamp", "vise", "level",
    
    # Nature & Plants
    "tree", "flower", "leaf", "rock", "stone", "shell", "feather", "nest", "branch",
    "seed", "pinecone", "acorn", "mushroom", "coral", "sand", "pebble",
    
    # Bathroom
    "toothbrush", "toothpaste", "floss", "bathtub", "shower", "toilet", "sink",
    "faucet", "drain", "plunger", "scale", "hairdryer", "straightener", "curler",
    
    # Appliances
    "washer", "dryer", "dishwasher", "freezer", "cooler", "humidifier", "dehumidifier",
    "airconditioner", "furnace", "waterheater", "garbagecan", "trashcan",
    
    # Communication & Media
    "book", "magazine", "newspaper", "poster", "sign", "billboard", "screen",
    "projector", "microphone", "megaphone", "album", "vinyl", "cassette", "disc",
    
    # Medical & Health
    "thermometer", "stethoscope", "bandage", "syringe", "crutch", "wheelchair",
    "glasses", "contacts", "inhaler", "mask", "gauze", "splint",
    
    # Building & Construction
    "brick", "cement", "beam", "column", "tile", "shingle", "gutter", "downspout",
    "insulation", "drywall", "plywood", "lumber", "girder",
    
    # Art & Craft
    "canvas", "easel", "palette", "paintbrush", "chisel", "clay", "yarn", "thread",
    "needle", "knitting", "crochet", "loom", "kiln", "pottery",
    
    # Safety & Emergency
    "extinguisher", "detector", "alarm", "siren", "flashlight", "flare", "vest",
    "harness", "lifejacket", "lifeboat", "parachute",
    
    # Seasonal & Holiday
    "ornament", "wreath", "garland", "lights", "stocking", "sleigh", "snowglobe",
    "menorah", "dreidel", "pumpkin", "haystack",
    
    # Structures & Architecture
    "door", "window", "wall", "floor", "ceiling", "roof", "stairs", "elevator",
    "escalator", "bridge", "tunnel", "monument", "lighthouse", "windmill", "castle",
    "tower", "pyramid", "temple", "mosque", "cathedral", "church", "synagogue",
    
    # Camping & Outdoor
    "tent", "sleeping", "lantern", "compass", "binoculars", "telescope", "microscope",
    "magnifying", "backpack", "canteen", "cooler", "grill", "campfire",
    
    # Time & Measurement
    "hourglass", "sundial", "stopwatch", "timer", "metronome", "odometer", "speedometer",
    "barometer", "hygrometer", "scale", "balance",
    
    # Sound & Music
    "gong", "bell", "horn", "siren", "chime", "whistle", "kazoo", "cowbell",
    
    # Symbols & Decoration
    "flag", "banner", "ribbon", "wreath", "crown", "scepter", "throne", "tiara",
    
    # Historical & Cultural
    "sword", "shield", "armor", "helmet", "spear", "bow", "arrow", "catapult",
    "cannon", "torch", "scroll", "quill", "inkwell",
    
    # Performance & Entertainment
    "mask", "costume", "puppet", "marionette", "prop", "backdrop", "curtain",
    
    # Industrial & Machinery
    "piston", "gear", "valve", "turbine", "generator", "engine", "motor", "pump",
    "conveyor", "crane", "pulley", "lever", "hoist"
]