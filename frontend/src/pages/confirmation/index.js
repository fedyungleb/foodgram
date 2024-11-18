import React from 'react';
import { Container, Main, Title } from '../../components';
import styles from './styles.module.css';
import MetaTags from 'react-meta-tags';
import { useLocation } from 'react-router-dom';

const Confirmation = () => {
  const location = useLocation();
  const { orderUuid } = location.state || {};

  return (
    <Main>
      <Container className={styles.container}>
        <MetaTags>
          <title>Order Confirmed</title>
          <meta name="description" content="Grocery Service Order Confirmation" />
        </MetaTags>
        <div className={styles.content}>
          <div className={styles.checkmark}>
            &#10003; {/* This renders a green checkmark */}
          </div>
          <Title title="Success!" />
          <p>Your order has been successfully created in the external grocery service.</p>
          {orderUuid && (
            <p className={styles.orderId}>
              <strong>Order ID:</strong> {orderUuid}
            </p>
          )}
        </div>
      </Container>
    </Main>
  );
};

export default Confirmation;
