import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { Card, Button, Chip, IconButton } from 'react-native-paper';
import { stockAPI, watchlistAPI } from '../services/api';
import { colors, spacing, typography, shadows } from '../constants/theme';

const StockDetailsScreen = ({ route, navigation }) => {
  const { symbol } = route.params;
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [addingToWatchlist, setAddingToWatchlist] = useState(false);

  useEffect(() => {
    fetchStockDetails();
  }, [symbol]);

  const fetchStockDetails = async () => {
    try {
      setLoading(true);
      const response = await stockAPI.getStockDetails(symbol);
      setStockData(response.data);
    } catch (error) {
      console.error('Error fetching stock details:', error);
      Alert.alert('Error', 'Failed to load stock details');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToWatchlist = async () => {
    try {
      setAddingToWatchlist(true);
      await watchlistAPI.addToWatchlist(
        stockData.symbol,
        stockData.name,
        stockData.current_price,
        'Added from stock details'
      );
      Alert.alert('Success', 'Stock added to watchlist');
    } catch (error) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to add to watchlist');
    } finally {
      setAddingToWatchlist(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  if (!stockData) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Stock data not available</Text>
      </View>
    );
  }

  const technical = stockData.technical_data || {};
  const fundamental = stockData.fundamental_data || {};
  const risk = stockData.risk_assessment || {};
  const recommendation = stockData.trading_recommendation || {};

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.symbol}>{stockData.symbol}</Text>
          <Text style={styles.name}>{stockData.name}</Text>
        </View>
        <IconButton
          icon="star-outline"
          size={28}
          iconColor={colors.primary}
          onPress={handleAddToWatchlist}
          disabled={addingToWatchlist}
        />
      </View>

      <Card style={styles.card}>
        <Card.Content>
          <Text style={styles.sectionTitle}>Current Price</Text>
          <Text style={styles.priceText}>₹{stockData.current_price?.toFixed(2)}</Text>
          <Text
            style={[
              styles.changeText,
              { color: technical.change_percent >= 0 ? colors.bullish : colors.bearish },
            ]}
          >
            {technical.change_percent >= 0 ? '+' : ''}{technical.change_percent?.toFixed(2)}%
          </Text>
        </Card.Content>
      </Card>

      {recommendation.action && (
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.sectionTitle}>Trading Recommendation</Text>
            <View style={styles.recommendationRow}>
              <Text style={styles.label}>Action:</Text>
              <Chip
                mode="flat"
                style={[
                  styles.actionChip,
                  {
                    backgroundColor:
                      recommendation.action === 'BUY'
                        ? colors.success
                        : recommendation.action === 'WAIT'
                        ? colors.warning
                        : colors.error,
                  },
                ]}
                textStyle={styles.actionText}
              >
                {recommendation.action}
              </Chip>
            </View>
            <View style={styles.row}>
              <Text style={styles.label}>Entry:</Text>
              <Text style={styles.value}>₹{recommendation.entry_price?.toFixed(2)}</Text>
            </View>
            <View style={styles.row}>
              <Text style={styles.label}>Stop Loss:</Text>
              <Text style={styles.value}>₹{recommendation.stop_loss?.toFixed(2)}</Text>
            </View>
            <View style={styles.row}>
              <Text style={styles.label}>Target:</Text>
              <Text style={styles.value}>₹{recommendation.target_price?.toFixed(2)}</Text>
            </View>
            <View style={styles.row}>
              <Text style={styles.label}>Risk:Reward:</Text>
              <Text style={[styles.value, { color: colors.success }]}>
                1:{recommendation.risk_reward_ratio?.toFixed(1)}
              </Text>
            </View>
          </Card.Content>
        </Card>
      )}

      <Card style={styles.card}>
        <Card.Content>
          <Text style={styles.sectionTitle}>Technical Indicators</Text>
          <View style={styles.indicatorsGrid}>
            <View style={styles.indicatorItem}>
              <Text style={styles.indicatorLabel}>RSI</Text>
              <Text style={styles.indicatorValue}>{technical.rsi?.toFixed(1) || 'N/A'}</Text>
            </View>
            <View style={styles.indicatorItem}>
              <Text style={styles.indicatorLabel}>MACD</Text>
              <Text style={styles.indicatorValue}>{technical.macd?.toFixed(2) || 'N/A'}</Text>
            </View>
            <View style={styles.indicatorItem}>
              <Text style={styles.indicatorLabel}>Volume Ratio</Text>
              <Text style={styles.indicatorValue}>{technical.volume_ratio?.toFixed(2) || 'N/A'}</Text>
            </View>
            <View style={styles.indicatorItem}>
              <Text style={styles.indicatorLabel}>ATR</Text>
              <Text style={styles.indicatorValue}>{technical.atr?.toFixed(2) || 'N/A'}</Text>
            </View>
          </View>
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text style={styles.sectionTitle}>Fundamental Data</Text>
          {fundamental.pe_ratio && (
            <View style={styles.row}>
              <Text style={styles.label}>P/E Ratio:</Text>
              <Text style={styles.value}>{fundamental.pe_ratio.toFixed(2)}</Text>
            </View>
          )}
          {fundamental.pb_ratio && (
            <View style={styles.row}>
              <Text style={styles.label}>P/B Ratio:</Text>
              <Text style={styles.value}>{fundamental.pb_ratio.toFixed(2)}</Text>
            </View>
          )}
          {fundamental.market_cap && (
            <View style={styles.row}>
              <Text style={styles.label}>Market Cap:</Text>
              <Text style={styles.value}>₹{(fundamental.market_cap / 10000000).toFixed(0)} Cr</Text>
            </View>
          )}
          {fundamental.sector && (
            <View style={styles.row}>
              <Text style={styles.label}>Sector:</Text>
              <Text style={styles.value}>{fundamental.sector}</Text>
            </View>
          )}
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text style={styles.sectionTitle}>Risk Assessment</Text>
          <View style={styles.riskRow}>
            <Text style={styles.label}>Risk Level:</Text>
            <Chip
              mode="flat"
              style={[
                styles.riskChip,
                {
                  backgroundColor:
                    risk.risk_level === 'Low'
                      ? colors.success
                      : risk.risk_level === 'Medium'
                      ? colors.warning
                      : colors.error,
                },
              ]}
              textStyle={styles.riskText}
            >
              {risk.risk_level || 'Medium'}
            </Chip>
          </View>
          <View style={styles.row}>
            <Text style={styles.label}>Risk Score:</Text>
            <Text style={styles.value}>{risk.risk_score?.toFixed(1) || 'N/A'}/10</Text>
          </View>
          <View style={styles.row}>
            <Text style={styles.label}>Volatility:</Text>
            <Text style={styles.value}>{((risk.volatility || 0) * 100).toFixed(1)}%</Text>
          </View>
        </Card.Content>
      </Card>

      <Button
        mode="contained"
        onPress={handleAddToWatchlist}
        loading={addingToWatchlist}
        disabled={addingToWatchlist}
        style={styles.addButton}
        buttonColor={colors.primary}
      >
        Add to Watchlist
      </Button>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.background,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.background,
  },
  errorText: {
    ...typography.body,
    color: colors.error,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.md,
    backgroundColor: colors.surface,
    ...shadows.small,
  },
  symbol: {
    ...typography.h2,
    color: colors.primary,
  },
  name: {
    ...typography.body,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
  card: {
    margin: spacing.md,
    backgroundColor: colors.surface,
    ...shadows.medium,
  },
  sectionTitle: {
    ...typography.h4,
    color: colors.primary,
    marginBottom: spacing.md,
  },
  priceText: {
    ...typography.h1,
    color: colors.text,
  },
  changeText: {
    ...typography.h4,
    fontWeight: '600',
    marginTop: spacing.xs,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.borderLight,
  },
  recommendationRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: spacing.sm,
    marginBottom: spacing.sm,
  },
  riskRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: spacing.sm,
    marginBottom: spacing.sm,
  },
  label: {
    ...typography.body,
    color: colors.textSecondary,
  },
  value: {
    ...typography.body,
    fontWeight: '600',
    color: colors.text,
  },
  actionChip: {},
  actionText: {
    color: colors.textWhite,
    fontWeight: '600',
  },
  riskChip: {},
  riskText: {
    color: colors.textWhite,
    fontWeight: '600',
  },
  indicatorsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.md,
  },
  indicatorItem: {
    width: '47%',
    padding: spacing.sm,
    backgroundColor: colors.background,
    borderRadius: 8,
    alignItems: 'center',
  },
  indicatorLabel: {
    ...typography.bodySmall,
    color: colors.textSecondary,
    marginBottom: spacing.xs,
  },
  indicatorValue: {
    ...typography.h4,
    color: colors.primary,
  },
  addButton: {
    margin: spacing.md,
    marginTop: spacing.sm,
  },
});

export default StockDetailsScreen;
