import React from 'react';
import { useHistory } from 'react-router-dom';
import styles from './styles.module.css'; // Existing styles
import { Title, Button } from '../../components'; // Reusing existing components

const LandingPage = () => {
  const history = useHistory();

  return (
    <div className={styles.container}>
      <div className={styles.overlay}>
        <div className={styles.content}>
          {/* Centered Title */}
          <Title title="Discover Recipes Like Never Before" className={styles.title}/>
          <p className={styles.subtitle}>
            Let our AI help you create amazing recipes tailored to your ingredients.<br/>
            Discover new dishes and unleash your culinary creativity!<br/>
            Explore the power of <strong>AI-driven recipe suggestions</strong> and transform your cooking experience.
          </p>
          <div className={styles.buttonGroup}>
            {/* Existing Button Components */}
            <Button
                modifier="style_dark-blue"
                clickHandler={() => history.push('/ai-suggestion')}
            >
              Try AI-Suggestion
            </Button>
            <Button
                modifier="style_dark-blue"
                clickHandler={() => history.push('/recipes')}
            >
              View Recipes
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
