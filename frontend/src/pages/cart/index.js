import { PurchaseList, Title, Container, Main, Button } from '../../components';
import styles from './styles.module.css';
import { useRecipes } from '../../utils/index.js';
import { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom'; // Import useHistory for React Router v5
import api from '../../api';
import MetaTags from 'react-meta-tags';

const Cart = ({ updateOrders, orders }) => {
  const { recipes, setRecipes, handleAddToCart } = useRecipes();
  const [isLoading, setIsLoading] = useState(false); // State for button loading
  const history = useHistory(); // Hook for navigation

  // Fetch recipes in the shopping cart
  const getRecipes = () => {
    api
      .getRecipes({
        page: 1,
        limit: 999,
        is_in_shopping_cart: Number(true),
      })
      .then((res) => {
        const { results } = res;
        setRecipes(results);
      });
  };

  useEffect(() => {
    getRecipes();
  }, []);

  // Download shopping list as a file
  const downloadDocument = () => {
    api.downloadFile();
  };

  // Handle checkout with the grocery service
  const handleCheckout = () => {
  setIsLoading(true); // Disable button during API call
  api
    .checkout()
    .then((res) => {
      setIsLoading(false);
      if (res.success) {
        // Navigate to Confirmation Page with order_uuid
        history.push('/confirmation', { orderUuid: res.order_uuid });
      } else {
        alert(`Error: ${res.message || 'Failed to complete checkout.'}`);
      }
    })
    .catch((err) => {
      setIsLoading(false);
      alert(`Error: ${err.error || 'Failed to complete checkout.'}`);
    });
};

  return (
    <Main>
      <Container className={styles.container}>
        <MetaTags>
          <title>Shopping list</title>
          <meta name="description" content="Grocery Assistant - Shopping List" />
          <meta property="og:title" content="Shopping list" />
        </MetaTags>
        <div className={styles.cart}>
          <Title title="Shopping list" />
          <PurchaseList
            orders={recipes}
            handleRemoveFromCart={handleAddToCart}
            updateOrders={updateOrders}
          />
          {orders > 0 && (
            <div className={styles.buttonGroup}>
              <Button
                modifier="style_dark-blue"
                clickHandler={downloadDocument}
              >
                Download list
              </Button>
              <Button
                modifier="style_dark-blue"
                clickHandler={handleCheckout}
                disabled={isLoading} // Disable button when loading
              >
                {isLoading ? 'Processing...' : 'Checkout with Grocery Service'}
              </Button>
            </div>
          )}
        </div>
      </Container>
    </Main>
  );
};

export default Cart;
