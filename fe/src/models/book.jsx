class Book {
  constructor(data) {
    this.id = data.id;
    this.title = data.title;
    this.author = data.author;
    this.imageUrl = data.image_url;
    this.description = data.description;
    this.price = data.price;
    this.total_quantity = data.total_quantity;
    this.available_quantity = data.available_quantity
  }

}

export default Book;