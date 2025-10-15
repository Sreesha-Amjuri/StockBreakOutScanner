import React from 'react';
import { StatusBar } from 'react-native';
import { Provider as PaperProvider } from 'react-native-paper';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { AuthProvider } from './src/utils/AuthContext';
import AppNavigator from './src/navigation/AppNavigator';
import { colors } from './src/constants/theme';

const App = () => {
  const theme = {
    colors: {
      primary: colors.primary,
      accent: colors.accent,
      background: colors.background,
      surface: colors.surface,
      text: colors.text,
      error: colors.error,
      disabled: colors.neutral,
      placeholder: colors.textLight,
      backdrop: 'rgba(0, 0, 0, 0.5)',
    },
  };

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <PaperProvider theme={theme}>
          <AuthProvider>
            <StatusBar
              barStyle="dark-content"
              backgroundColor={colors.background}
            />
            <AppNavigator />
          </AuthProvider>
        </PaperProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
};

export default App;
