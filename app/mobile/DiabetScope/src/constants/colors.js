/**
 * colors.js
 * ─────────
 * Centralized color palette for the entire app.
 * 
 * WHY centralize colors?
 *   • Consistency across all screens
 *   • Easy theme changes (just edit here)
 *   • Professional appearance
 */

export const COLORS = {
  // Primary brand colors
  primary: '#2563EB',      // Blue - main actions, buttons
  primaryDark: '#1E40AF',  // Darker blue - button press states
  primaryLight: '#DBEAFE', // Light blue - backgrounds, highlights
  
  // Success/Warning/Error
  success: '#10B981',      // Green - positive results, success messages
  warning: '#F59E0B',      // Amber - warnings, caution
  error: '#EF4444',        // Red - errors, high-risk alerts
  
  // Neutral colors
  background: '#F9FAFB',   // Off-white - app background
  cardBackground: '#FFFFFF', // Pure white - cards, input fields
  border: '#E5E7EB',       // Light gray - borders, dividers
  
  // Text colors
  textPrimary: '#111827',  // Almost black - headings, primary text
  textSecondary: '#6B7280', // Gray - secondary text, labels
  textMuted: '#9CA3AF',    // Light gray - placeholders, disabled text
  
  // Result-specific colors
  diabetic: '#DC2626',     // Dark red - diabetic prediction
  nonDiabetic: '#059669',  // Dark green - non-diabetic prediction
  
  // Overlay
  overlay: 'rgba(0, 0, 0, 0.5)', // Semi-transparent black - modals
};

export default COLORS;
