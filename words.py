import random
words = ["apple", "pear", "hitler", "banana", "tomato","adolf", "cabbage", "cloud", "piece", "paper", "spring", "earth", "water", "tulip", "chair", "key", "flower", "sun", "moon", "house", "window", "door", "dog", "cat", "clock", "light", "picture", "word", "pen", "glass", "work", "city", "forest", "river", "sea", "boat", "bridge", "sound", "music", "dance", "color", "lunch", "heart", "fish", "coal", "desert", "grass", "book", "notebook", "wind", "shadow", "garden", "faith", "joy", "sadness", "bottle", "sand", "snow", "rain", "bird", "owl", "chicken", "world", "love", "friendship", "time", "mountain", "valley", "road", "winter", "summer", "autumn", "flower", "campfire", "stone", "ball", "play", "laughter", "bread", "cheese", "frog", "motorcycle", "bicycle", "car", "armchair", "wardrobe", "bed", "dresser", "appletree", "radiator", "glasses", "hat", "shoes", "pig", "scissors", "needle", "thread", "salt", "sugar", "footballer", "actor", "princess", "castle", "king", "queen", "turtle", "crocodile", "lamp", "nature", "lamp", "television", "tiger", "lion", "wolf", "snowball", "snowman", "watch", "computer", "phone", "keyboard", "mouse", "battery", "flashlight", "cover", "newspaper"]

def choose_word():
    return random.choice(words)

if __name__ == "__main__":
    print(type(choose_word()))