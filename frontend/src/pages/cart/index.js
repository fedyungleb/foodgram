import Modal from 'react-modal';
import {useState, useEffect} from 'react';
import {PurchaseList, Title, Container, Main, Button} from '../../components';
import styles from './styles.module.css';
import {useRecipes} from '../../utils/index.js';
import {useHistory} from 'react-router-dom'; // Import useHistory for React Router v5
import api from '../../api';

const Cart = ({updateOrders, orders}) => {
    const {recipes, setRecipes, handleAddToCart} = useRecipes();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedService, setSelectedService] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const history = useHistory();

    const deliveryServices = [
        {name: 'Barbora', value: 'barbora', enabled: true},
        {name: 'Cash&Carry', value: 'cashcarry', enabled: false},
        {name: 'BoltMarket', value: 'boltmarket', enabled: true},
    ];

    // Fetch recipes in the shopping cart
    const getRecipes = () => {
        api
            .getRecipes({
                page: 1,
                limit: 999,
                is_in_shopping_cart: Number(true),
            })
            .then((res) => {
                const {results} = res;
                console.log('Fetched Recipes:', results); // Debugging log
                setRecipes(results);
            })
            .catch((err) => {
                console.error('Error fetching recipes:', err); // Debugging log
            });
    };

    useEffect(() => {
        getRecipes();
    }, []);

    const confirmCheckout = () => {
        setIsModalOpen(false);
        setIsLoading(true);

        api
            .checkout()
            .then((res) => {
                setIsLoading(false);
                if (res.success) {
                    // Update recipes and navigate to confirmation page
                    const purchasedRecipeIds = res.purchased_recipes || [];
                    setRecipes((prevRecipes) =>
                        prevRecipes.filter((recipe) => !purchasedRecipeIds.includes(recipe.id))
                    );
                    history.push('/confirmation', {orderUuid: res.order_uuid});
                } else {
                    alert(`Error: ${res.message || 'Failed to complete checkout.'}`);
                }
            })
            .catch((err) => {
                setIsLoading(false);
                console.error('Error during checkout:', err); // Debugging log
                alert(`Error: ${err.error || 'Failed to complete checkout.'}`);
            });
    };

    return (
        <Main>
            <Container className={styles.container}>
                <Title title="Shopping List"/>
                <PurchaseList
                    orders={recipes}
                    handleRemoveFromCart={handleAddToCart}
                    updateOrders={updateOrders}
                />
                {orders > 0 && (
                    <div className={styles.buttonGroup}>
                        <div className={styles.dropdown}>
                            <label htmlFor="deliveryService">Choose Delivery Service:</label>
                            <select
                                id="deliveryService"
                                value={selectedService}
                                onChange={(e) => setSelectedService(e.target.value)}
                            >
                                <option value="" disabled>
                                    Select a service
                                </option>
                                {deliveryServices.map((service) => (
                                    <option
                                        key={service.value}
                                        value={service.value}
                                        disabled={!service.enabled}
                                    >
                                        {service.name} {service.enabled ? '' : '(Unavailable)'}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <Button
                            modifier="style_dark-blue"
                            clickHandler={() => {
                                console.log('Opening modal'); // Debugging log
                                setIsModalOpen(true);
                            }}
                            disabled={!selectedService || isLoading}
                        >
                            {isLoading ? 'Processing...' : 'Checkout'}
                        </Button>
                    </div>
                )}
                <Modal
                    isOpen={isModalOpen}
                    onRequestClose={() => setIsModalOpen(false)}
                    contentLabel="Confirm Checkout"
                    className={styles.modal}
                    overlayClassName={styles.overlay}
                >
                    <h2>Confirm Checkout</h2>
                    <p>{recipes.length > 0 ? "Ingredients in your shopping list:" : "No recipes found."}</p>
                    <ul>
                        {recipes.map((recipe) => (
                            <li key={recipe.id}>
                                <strong>{recipe.name}</strong>
                                <ul>
                                    {recipe.ingredients.map((ingredient) => (
                                        <li key={ingredient.id}>
                                            {ingredient.name} - {ingredient.amount} {ingredient.measurement_unit}
                                        </li>
                                    ))}
                                </ul>
                            </li>
                        ))}
                    </ul>
                    <p>
                        Proceed with{' '}
                        {deliveryServices.find((s) => s.value === selectedService)?.name}?
                    </p> {/* Adding the question here */}
                    <div className={styles.modalButtons}>
                        <Button modifier="style_dark-blue" clickHandler={confirmCheckout}>
                            Yes
                        </Button>
                        <Button modifier="style_red" clickHandler={() => setIsModalOpen(false)}>
                            No
                        </Button>
                    </div>
                </Modal>
            </Container>
        </Main>
    );
};

export default Cart;
