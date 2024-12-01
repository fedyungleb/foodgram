import React, { useContext, useState } from 'react';
import { Container, Main, Title, Button } from '../../components';
import styles from './styles.module.css'; // Import the styles
import { AiSuggestionContext } from '../../contexts';

const AiSuggestion = () => {
  const { ingredients, setIngredients, suggestion, setSuggestion } = useContext(AiSuggestionContext);
  const [loading, setLoading] = useState(false); // Add loading state

  const handleSubmit = () => {
    setLoading(true); // Set loading to true when the request starts
    fetch('/api/recipes/ai-suggestion/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ingredients }),
    })
      .then((res) => res.json())
      .then((data) => {
        setSuggestion(data.suggestion || '');
        setLoading(false); // Set loading to false after getting the response
      })
      .catch((err) => {
        console.error(err);
        setLoading(false); // Set loading to false if there is an error
      });
  };

  return (
    <Main>
      <Container className={styles.container}>
        <Title title="AI Recipe Suggestions" />
        <textarea
          placeholder="Enter ingredients (e.g., chicken, rice, broccoli)"
          value={ingredients}
          onChange={(e) => setIngredients(e.target.value)}
          className={styles.textarea}
        />
        <Button
          modifier="style_dark-blue"
          clickHandler={handleSubmit}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Get Suggestion'}
        </Button>
        {suggestion && (
          <div className={styles.suggestion}>
            <h2>Suggested Recipe</h2>
            <pre>{suggestion}</pre>
          </div>
        )}
      </Container>
    </Main>
  );
};

export default AiSuggestion;
