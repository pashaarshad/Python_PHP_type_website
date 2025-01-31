from flask import Flask, render_template_string, request, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Mock product database as a list
products = []

# HTML templates within the Python file
home_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Product Gallery</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5>
        <h1 class="text-center">Product Gallery</h1>
        <a class="btn btn-primary mb-3" href="/add">Add New Product</a>
        <div class="row">
            {% for product in products %}
            <div class="col-md-4">
                <div class="card mb-4">
                    <img src="{{ product.image }}" class="card-img-top" alt="Product Image">
                    <div class="card-body">
                        <h5 class="card-title">{{ product.name }}</h5>
                        <p clas="card-text">{{ product.description }}</p>
                        <p class="card-text text-muted">Price: ${{ product.price }}</p>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

add_product_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Add Product</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">        <h1>Add New Product</h1>
        <form action="/add" method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label for="name">Product Name:</label>
                <input type="text" class="form-control" name="name" required>
            </div>
            <div class="form-group">
                <label for="price">Price:</label>
                <input type="number" class="form-control" name="price" required>
            </div>
            <div class="frm-group">
                <label for="description">Description:</label>
                <textarea class="form-control" name="description" required></textarea>
            </div>
            <div class="form-group">
                <label for="image">Image:</label>
                <input type="file" class="form-control" name="image" required>
            </div>
            <button type="submit" class="btn btn-success">Add Product</button>
        </form>
        <a href="/" class="btn btn-secondary mt-3"Back to Home</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(home_page, products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image = request.files['image']
        
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            products.append({
                'name': name,
                'price': price,
                'description': description,
                'image': '/' + image_path
            })
        
        return redirect(url_for('home'))
    
    return render_template_string(add_product_page)

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
    @app.route('/delete/<int:product_id>', methods=['POST'])
    def delete_product(product_id):
        if 0 <= product_id < len(products):
            del products[product_id]
        return redirect(url_for('home'))