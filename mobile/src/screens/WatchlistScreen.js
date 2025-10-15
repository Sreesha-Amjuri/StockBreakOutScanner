import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  RefreshControl,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { Card, FAB, IconButton } from 'react-native-paper';
import { watchlistAPI } from '../services/api';
import { colors, spacing, typography, shadows } from '../constants/theme';

const WatchlistScreen = ({ navigation }) => {
  const [watchlist, setWatchlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchWatchlist();
  }, []);

  const fetchWatchlist = async () => {
    try {
      setLoading(true);
      const response = await watchlistAPI.getWatchlist();
      setWatchlist(response.data || []);
    } catch (error) {
      console.error('Error fetching watchlist:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchWatchlist();
    setRefreshing(false);
  };

  const handleRemove = async (id, symbol) => {
    Alert.alert(
      'Remove from Watchlist',
      `Are you sure you want to remove ${symbol}?`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Remove',
          style: 'destructive',
          onPress: async () => {
            try {
              await watchlistAPI.removeFromWatchlist(id);
              setWatchlist(watchlist.filter((item) => item.id !== id));
            } catch (error) {
              Alert.alert('Error', 'Failed to remove from watchlist');
            }
          },
        },
      ]
    );
  };

  const renderWatchlistCard = ({ item }) => (
    <TouchableOpacity
      activeOpacity={0.7}
      onPress={() => navigation.navigate('StockDetails', { symbol: item.symbol })}
    >
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.cardHeader}>
            <View style={styles.stockInfo}>
              <Text style={styles.symbol}>{item.symbol}</Text>
              <Text style={styles.name}>{item.name}</Text>
            </View>
            <IconButton
              icon="delete-outline"
              size={24}
              iconColor={colors.error}
              onPress={() => handleRemove(item.id, item.symbol)}
            />
          </View>

          <View style={styles.priceRow}>
            <View>
              <Text style={styles.label}>Added Price</Text>
              <Text style={styles.price}>₹{item.added_price?.toFixed(2)}</Text>
            </View>
            {item.target_price && (
              <View>
                <Text style={styles.label}>Target</Text>
                <Text style={[styles.price, { color: colors.success }]}>
                  ₹{item.target_price?.toFixed(2)}
                </Text>
              </View>
            )}
            {item.stop_loss && (
              <View>
                <Text style={styles.label}>Stop Loss</Text>
                <Text style={[styles.price, { color: colors.error }]}>
                  ₹{item.stop_loss?.toFixed(2)}
                </Text>
              </View>
            )}
          </View>

          {item.notes && (
            <View style={styles.notesContainer}>
              <Text style={styles.notesLabel}>Notes:</Text>
              <Text style={styles.notes}>{item.notes}</Text>
            </View>
          )}

          <Text style={styles.addedDate}>
            Added: {new Date(item.added_date).toLocaleDateString()}
          </Text>
        </Card.Content>
      </Card>
    </TouchableOpacity>
  );

  if (loading && !refreshing) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={watchlist}
        renderItem={renderWatchlistCard}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={[colors.primary]}
          />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>Your watchlist is empty</Text>
            <Text style={styles.emptySubtext}>
              Add stocks from the dashboard or search
            </Text>
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
  listContent: {
    padding: spacing.md,
  },
  card: {
    marginBottom: spacing.md,
    backgroundColor: colors.surface,
    ...shadows.medium,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: spacing.md,
  },
  stockInfo: {
    flex: 1,
  },
  symbol: {
    ...typography.h3,
    color: colors.primary,
  },
  name: {
    ...typography.bodySmall,
    marginTop: spacing.xs,
  },
  priceRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.md,
  },
  label: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  price: {
    ...typography.body,
    fontWeight: '600',
    marginTop: spacing.xs,
  },
  notesContainer: {
    marginBottom: spacing.sm,
  },
  notesLabel: {
    ...typography.bodySmall,
    fontWeight: '600',
    marginBottom: spacing.xs,
  },
  notes: {
    ...typography.bodySmall,
    color: colors.textSecondary,
  },
  addedDate: {
    ...typography.caption,
    color: colors.textLight,
  },
  emptyContainer: {
    alignItems: 'center',
    padding: spacing.xl,
    paddingTop: spacing.xxl,
  },
  emptyText: {
    ...typography.h4,
    color: colors.textSecondary,
    marginBottom: spacing.sm,
  },
  emptySubtext: {
    ...typography.body,
    color: colors.textLight,
    textAlign: 'center',
  },
  fab: {
    position: 'absolute',
    right: spacing.md,
    bottom: spacing.md,
    backgroundColor: colors.primary,
  },
});

export default WatchlistScreen;
