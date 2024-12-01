import React, { useState, useEffect } from 'react';
import { Switch, Route, useHistory, Redirect, useLocation } from 'react-router-dom';
import './App.css';
import { Header, Footer, ProtectedRoute } from './components';
import api from './api';
import styles from './styles.module.css';
import cn from 'classnames';
import hamburgerImg from './images/hamburger-menu.png';
import Modal from 'react-modal'

import {
  Main,
  Cart,
  SignIn,
  Subscriptions,
  Favorites,
  SingleCard,
  SignUp,
  RecipeEdit,
  RecipeCreate,
  User,
  ChangePassword,
  Confirmation,
  AiSuggestion, // Import AI Suggestion page
} from './pages';
import { AuthContext, UserContext, AiSuggestionContext } from './contexts';

function App() {
  useEffect(() => {
    Modal.setAppElement('#root');
  }, []);
  const [loggedIn, setLoggedIn] = useState(null);
  const [user, setUser] = useState({});
  const [orders, setOrders] = useState(0);
  const [recipes, setRecipes] = useState([]);
  const [menuToggled, setMenuToggled] = useState(false);
  const location = useLocation();
  const history = useHistory();

  const [ingredients, setIngredients] = useState('');
  const [suggestion, setSuggestion] = useState('');
  const [isLoading, setIsLoading] = useState(false); // Fixed declaration of isLoading
  useEffect(() => {
  getOrders();
}, []);
  const registration = ({ email, password, username, first_name, last_name }) => {
    api
      .signup({ email, password, username, first_name, last_name })
      .then(() => {
        history.push('/signin');
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          alert(errors.join(', '));
        }
        setLoggedIn(false);
      });
  };

  const changePassword = ({ new_password, current_password }) => {
    api
      .changePassword({ new_password, current_password })
      .then(() => {
        history.push('/signin');
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          alert(errors.join(', '));
        }
      });
  };

  const authorization = ({ email, password }) => {
    api
      .signin({ email, password })
      .then((res) => {
        if (res.auth_token) {
          localStorage.setItem('token', res.auth_token);
          api
            .getUserData()
            .then((res) => {
              setUser(res);
              setLoggedIn(true);
              getOrders();
            })
            .catch(() => {
              setLoggedIn(false);
              history.push('/signin');
            });
        } else {
          setLoggedIn(false);
        }
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          alert(errors.join(', '));
        }
        setLoggedIn(false);
      });
  };

  const onSignOut = () => {
    api
      .signout()
      .then(() => {
        localStorage.removeItem('token');
        setLoggedIn(false);
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          alert(errors.join(', '));
        }
      });
  };

  const getOrders = () => {
  api
    .getRecipes({
      page: 1,
      is_in_shopping_cart: Number(true),
    })
    .then((res) => {
      const { results } = res; // Extract the recipes from the API response
      setRecipes(results); // Set the recipes (with ingredients) in the state
      const { count } = res; // Optionally, extract the count for orders
      setOrders(count); // Update the orders count
    })
    .catch((err) => {
      console.error('Error fetching orders:', err); // Log any errors
    });
};


  const updateOrders = (add) => {
    if (!add && orders <= 0) {
      return;
    }
    setOrders(add ? orders + 1 : orders - 1);
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      api
        .getUserData()
        .then((res) => {
          setUser(res);
          setLoggedIn(true);
          getOrders();
        })
        .catch(() => {
          setLoggedIn(false);
          history.push('/signin');
        });
    } else {
      setLoggedIn(false);
    }
  }, []);

  const handleCheckout = () => {
    console.log('Checkout initiated');
    setIsLoading(true); // Disable button during API call
    api
      .checkout()
      .then((res) => {
        console.log('API response:', res);
        setIsLoading(false);
        if (res.success) {
          history.push('/confirmation', { orderUuid: res.order_uuid });
        } else {
          alert(`Error: ${res.message || 'Failed to complete checkout.'}`);
        }
      })
      .catch((err) => {
        console.error('API error:', err);
        setIsLoading(false);
        alert(`Error: ${err.error || 'Failed to complete checkout.'}`);
      });
  };

  if (loggedIn === null) {
    return <div className={styles.loading}>Loading!!</div>;
  }

  return (
    <AuthContext.Provider value={loggedIn}>
      <UserContext.Provider value={user}>
        <AiSuggestionContext.Provider
          value={{ ingredients, setIngredients, suggestion, setSuggestion }}
        >
          <div
            className={cn('App', {
              [styles.appMenuToggled]: menuToggled,
            })}
          >
            <div className={styles.menuButton} onClick={() => setMenuToggled(!menuToggled)}>
              <img src={hamburgerImg} alt="Menu" />
            </div>
            <Header orders={orders} loggedIn={loggedIn} onSignOut={onSignOut} />
            <Switch>
              <ProtectedRoute
                exact
                path="/user/:id"
                component={User}
                loggedIn={loggedIn}
                updateOrders={updateOrders}
              />
              <ProtectedRoute
                exact
                path="/cart"
                component={Cart}
                orders={orders}
                loggedIn={loggedIn}
                updateOrders={updateOrders}
              />
              <Route exact path="/confirmation">
                <Confirmation />
              </Route>
              <ProtectedRoute
                exact
                path="/subscriptions"
                component={Subscriptions}
                loggedIn={loggedIn}
              />
              <ProtectedRoute
                exact
                path="/favorites"
                component={Favorites}
                loggedIn={loggedIn}
                updateOrders={updateOrders}
              />
              <ProtectedRoute
                exact
                path="/recipes/create"
                component={RecipeCreate}
                loggedIn={loggedIn}
              />
              <ProtectedRoute
                exact
                path="/recipes/:id/edit"
                component={RecipeEdit}
                loggedIn={loggedIn}
                onItemDelete={getOrders}
              />
              <ProtectedRoute
                exact
                path="/change-password"
                component={ChangePassword}
                loggedIn={loggedIn}
                onPasswordChange={changePassword}
              />
              <Route exact path="/recipes/:id">
                <SingleCard loggedIn={loggedIn} updateOrders={updateOrders} />
              </Route>
              <Route exact path="/recipes">
                <Main updateOrders={updateOrders} />
              </Route>
              <Route exact path="/signin">
                <SignIn onSignIn={authorization} />
              </Route>
              <Route exact path="/signup">
                <SignUp onSignUp={registration} />
              </Route>
              <Route exact path="/ai-suggestion">
                <AiSuggestion />
              </Route>
              <Route path="/">
                {loggedIn ? <Redirect to="/recipes" /> : <Redirect to="/signin" />}
              </Route>
            </Switch>
            <Footer />
          </div>
        </AiSuggestionContext.Provider>
      </UserContext.Provider>
    </AuthContext.Provider>
  );
}

export default App;
