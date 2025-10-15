// Elegant Pastel Color Theme for StockBreak Pro
export const colors = {
  // Primary pastel colors
  primary: '#9B8DC7',        // Soft purple
  primaryDark: '#7B6BA3',    // Darker purple
  primaryLight: '#C5B8E0',   // Lighter purple
  
  // Secondary pastel colors
  secondary: '#A8D5BA',      // Soft green
  secondaryDark: '#88B59A',  // Darker green
  secondaryLight: '#C8E5D4', // Lighter green
  
  // Accent colors
  accent: '#FFB4A9',         // Soft coral
  accentDark: '#DF9489',     // Darker coral
  accentLight: '#FFC4B9',    // Lighter coral
  
  // Background colors
  background: '#F8F6FA',     // Very light purple
  surface: '#FFFFFF',        // White
  card: '#FDFCFE',           // Off white
  
  // Status colors (pastel versions)
  success: '#A8D5BA',        // Soft green
  warning: '#FFD6A5',        // Soft orange
  error: '#FFB4A9',          // Soft red
  info: '#A8C8E7',           // Soft blue
  
  // Text colors
  text: '#4A4A4A',           // Dark gray
  textSecondary: '#757575',  // Medium gray
  textLight: '#9E9E9E',      // Light gray
  textWhite: '#FFFFFF',      // White
  
  // Chart colors (pastel)
  chartPrimary: '#9B8DC7',
  chartSecondary: '#A8D5BA',
  chartTertiary: '#FFB4A9',
  chartQuaternary: '#A8C8E7',
  
  // Additional colors
  bullish: '#A8D5BA',        // Soft green for gains
  bearish: '#FFB4A9',        // Soft red for losses
  neutral: '#C5C5C5',        // Gray
  
  // Border colors
  border: '#E6E1EC',         // Light purple border
  borderLight: '#F0EBF5',    // Very light purple border
  
  // Shadow colors
  shadow: 'rgba(155, 141, 199, 0.15)',
  shadowDark: 'rgba(155, 141, 199, 0.25)',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const borderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  round: 999,
};

export const typography = {
  h1: {
    fontSize: 32,
    fontWeight: 'bold',
    color: colors.text,
  },
  h2: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.text,
  },
  h3: {
    fontSize: 20,
    fontWeight: '600',
    color: colors.text,
  },
  h4: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
  },
  body: {
    fontSize: 16,
    color: colors.text,
  },
  bodySmall: {
    fontSize: 14,
    color: colors.textSecondary,
  },
  caption: {
    fontSize: 12,
    color: colors.textLight,
  },
};

export const shadows = {
  small: {
    shadowColor: colors.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 3,
    elevation: 2,
  },
  medium: {
    shadowColor: colors.shadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 5,
    elevation: 4,
  },
  large: {
    shadowColor: colors.shadowDark,
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 6,
  },
};

export default {
  colors,
  spacing,
  borderRadius,
  typography,
  shadows,
};
