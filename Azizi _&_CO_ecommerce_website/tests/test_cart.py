def test_add_to_cart(client, db):
    """Test adding a product to the shopping session cart."""
    # Simulate adding product ID 1 to cart via session mock
    with client.session_transaction() as sess:
        sess['cart'] = {str(1): 2}  # 2 units of product 1

    # Check that context processor counter reads 2 items total
    response = client.get('/')
    assert response.status_code == 200
    # The cart badge counter injection should reflect 2
    assert b'2' in response.data