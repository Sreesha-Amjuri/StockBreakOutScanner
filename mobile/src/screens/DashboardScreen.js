import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  RefreshControl,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { Card, Chip, FAB, Searchbar } from 'react-native-paper';
import { stockAPI } from '../services/api';
import { colors, spacing, typography, shadows } from '../constants/theme';
import { useAuth } from '../utils/AuthContext';

const DashboardScreen = ({ navigation }) => {
  const [breakouts, setBreakouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [scanStats, setScanStats] = useState({ stocks_scanned: 0, breakouts_found: 0 });
  const { logout } = useAuth();

  useEffect(() => {
    fetchBreakouts();
  }, []);

  const fetchBreakouts = async () => {
    try {
      setLoading(true);
      const response = await stockAPI.scanBreakouts({ limit: 20, min_confidence: 0.6 });
      setBreakouts(response.data.breakout_stocks || []);
      setScanStats(response.data.scan_statistics || { stocks_scanned: 0, breakouts_found: 0 });
    } catch (error) {
      console.error('Error fetching breakouts:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchBreakouts();
    setRefreshing(false);
  };

  const filteredBreakouts = breakouts.filter(
    (stock) =>
      stock.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
      stock.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const renderStockCard = ({ item }) => (
    <TouchableOpacity
      activeOpacity={0.7}
      onPress={() => navigation.navigate('StockDetails', { symbol: item.symbol })}
    >
      <Card style={styles.stockCard}>
        <Card.Content>
          <View style={styles.cardHeader}>
            <View style={styles.stockInfo}>
              <Text style={styles.symbol}>{item.symbol}</Text>
              <Text style={styles.stockName}>{item.name}</Text>
            </View>
            <View style={styles.priceContainer}>
              <Text style={styles.price}>₹{item.current_price?.toFixed(2)}</Text>
              <Text
                style={[
                  styles.change,
                  { color: item.technical_data?.change_percent >= 0 ? colors.bullish : colors.bearish },
                ]}
              >
                {item.technical_data?.change_percent >= 0 ? '+' : ''}
                {item.technical_data?.change_percent?.toFixed(2)}%
              </Text>
            </View>
          </View>

          <View style={styles.indicators}>
            <View style={styles.indicatorRow}>
              <Text style={styles.indicatorLabel}>RSI:</Text>
              <Text style={styles.indicatorValue}>{item.technical_data?.rsi?.toFixed(1) || 'N/A'}</Text>
            </View>
            <View style={styles.indicatorRow}>
              <Text style={styles.indicatorLabel}>Confidence:</Text>
              <Text style={[styles.indicatorValue, styles.confidence]}>
                {((item.confidence_score || 0) * 100).toFixed(0)}%
              </Text>
            </View>
          </View>

          <View style={styles.chips}>
            <Chip
              mode="flat"
              style={styles.chip}
              textStyle={styles.chipText}
              selectedColor={colors.primary}
            >
              {item.breakout_type || 'Breakout'}
            </Chip>
            {item.sector && (
              <Chip
                mode="flat"
                style={styles.chip}
                textStyle={styles.chipText}
                selectedColor={colors.secondary}
              >
                {item.sector}
              </Chip>
            )}
          </View>

          {item.trading_recommendation?.action && (
            <View style={styles.recommendation}>
              <Text style={styles.recommendationLabel}>Action:</Text>
              <Chip
                mode="flat"
                style={[
                  styles.actionChip,
                  { backgroundColor: item.trading_recommendation.action === 'BUY' ? colors.success : colors.warning },
                ]}
                textStyle={styles.actionText}
              >
                {item.trading_recommendation.action}
              </Chip>
            </View>
          )}
        </Card.Content>
      </Card>
    </TouchableOpacity>
  );

  if (loading && !refreshing) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={colors.primary} />
        <Text style={styles.loadingText}>Scanning stocks...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>StockBreak Pro</Text>
        <TouchableOpacity onPress={logout} style={styles.logoutButton}>
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.statsContainer}>
        <Card style={styles.statCard}>
          <Card.Content style={styles.statContent}>
            <Text style={styles.statValue}>{scanStats.stocks_scanned}</Text>
            <Text style={styles.statLabel}>Scanned</Text>
          </Card.Content>
        </Card>
        <Card style={styles.statCard}>
          <Card.Content style={styles.statContent}>
            <Text style={[styles.statValue, { color: colors.success }]}>{scanStats.breakouts_found}</Text>
            <Text style={styles.statLabel}>Breakouts</Text>
          </Card.Content>
        </Card>
      </View>

      <Searchbar
        placeholder="Search stocks..."
        onChangeText={setSearchQuery}
        value={searchQuery}
        style={styles.searchbar}
        iconColor={colors.primary}
        inputStyle={styles.searchInput}
      />

      <FlatList
        data={filteredBreakouts}
        renderItem={renderStockCard}
        keyExtractor={(item) => item.symbol}
        contentContainerStyle={styles.listContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={[colors.primary]} />}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>No breakouts found</Text>
          </View>
        }
      />

      <FAB
        icon="refresh"
        style={styles.fab}
        color={colors.textWhite}
        onPress={onRefresh}
      />
    </View>
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
  loadingText: {
    ...typography.body,
    marginTop: spacing.md,
    color: colors.textSecondary,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.md,
    backgroundColor: colors.surface,
    ...shadows.small,
  },
  title: {
    ...typography.h2,
    color: colors.primary,
  },
  logoutButton: {
    padding: spacing.sm,
  },
  logoutText: {
    color: colors.error,
    fontSize: 14,
    fontWeight: '600',
  },
  statsContainer: {
    flexDirection: 'row',
    padding: spacing.md,
    gap: spacing.md,
  },
  statCard: {
    flex: 1,
    backgroundColor: colors.surface,
    ...shadows.small,
  },
  statContent: {
    alignItems: 'center',
  },
  statValue: {
    ...typography.h2,
    color: colors.primary,
  },
  statLabel: {
    ...typography.bodySmall,
    marginTop: spacing.xs,
  },
  searchbar: {
    marginHorizontal: spacing.md,
    marginBottom: spacing.md,
    backgroundColor: colors.surface,
    elevation: 2,
  },
  searchInput: {
    color: colors.text,
  },
  listContent: {
    padding: spacing.md,
  },
  stockCard: {
    marginBottom: spacing.md,
    backgroundColor: colors.surface,
    ...shadows.medium,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.md,
  },
  stockInfo: {
    flex: 1,
  },
  symbol: {
    ...typography.h3,
    color: colors.primary,
  },
  stockName: {
    ...typography.bodySmall,
    marginTop: spacing.xs,
  },
  priceContainer: {
    alignItems: 'flex-end',
  },
  price: {
    ...typography.h4,
  },
  change: {
    ...typography.body,
    fontWeight: '600',
    marginTop: spacing.xs,
  },
  indicators: {
    flexDirection: 'row',
    gap: spacing.lg,
    marginBottom: spacing.md,
  },
  indicatorRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  indicatorLabel: {
    ...typography.bodySmall,
    marginRight: spacing.xs,
  },
  indicatorValue: {
    ...typography.body,
    fontWeight: '600',
  },
  confidence: {
    color: colors.success,
  },
  chips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginBottom: spacing.sm,
  },
  chip: {
    backgroundColor: colors.primaryLight,
  },
  chipText: {
    fontSize: 12,
    color: colors.primaryDark,
  },
  recommendation: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: spacing.sm,
  },
  recommendationLabel: {
    ...typography.bodySmall,
    marginRight: spacing.sm,
  },
  actionChip: {},
  actionText: {
    color: colors.textWhite,
    fontWeight: '600',
    fontSize: 12,
  },
  emptyContainer: {
    alignItems: 'center',
    padding: spacing.xl,
  },
  emptyText: {
    ...typography.body,
    color: colors.textSecondary,
  },
  fab: {
    position: 'absolute',
    right: spacing.md,
    bottom: spacing.md,
    backgroundColor: colors.primary,
  },
});

export default DashboardScreen;
