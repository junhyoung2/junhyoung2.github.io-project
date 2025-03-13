function getRandomFood() {
    const foods = ["Pizza", "Burger", "Sushi", "Pasta", "Tacos", "Ramen", "Salad", "Steak", "Sandwich", "Dumplings"];
    const randomIndex = Math.floor(Math.random() * foods.length);
    return foods[randomIndex];
}

console.log("Random Food:", getRandomFood());
