/**
 * validators.js
 * ─────────────
 * Input validation utilities.
 * 
 * WHY validate on frontend?
 *   • Instant feedback to user (better UX)
 *   • Prevent unnecessary API calls
 *   • Match backend validation (Pydantic schemas)
 * 
 * Each validator matches the constraints in backend/schemas.py
 */

/**
 * Validate a single numeric field.
 * 
 * @param {string} value - Raw input value
 * @param {number} min - Minimum allowed value (inclusive)
 * @param {number} max - Maximum allowed value (inclusive)
 * @param {boolean} allowZero - Whether zero is valid (for optional measurements)
 * @returns {object} { valid: boolean, error: string|null }
 */
export const validateNumericField = (value, min, max, allowZero = true) => {
  // Check if empty
  if (value === '' || value === null || value === undefined) {
    return { valid: false, error: 'This field is required' };
  }
  
  // Check if numeric
  const num = parseFloat(value);
  if (isNaN(num)) {
    return { valid: false, error: 'Must be a number' };
  }
  
  // Check zero constraint
  if (num === 0 && !allowZero) {
    return { valid: false, error: 'Must be greater than 0' };
  }
  
  // Check range
  if (num < min) {
    return { valid: false, error: `Must be at least ${min}` };
  }
  if (num > max) {
    return { valid: false, error: `Must be at most ${max}` };
  }
  
  return { valid: true, error: null };
};

/**
 * Validate all diabetes prediction inputs (classification).
 * 
 * Constraints match backend/schemas.py DiabetesInput.
 */
export const validateDiabetesInputs = (inputs) => {
  const errors = {};
  
  // Pregnancies: 0-20, zero allowed
  const pregnancies = validateNumericField(inputs.pregnancies, 0, 20, true);
  if (!pregnancies.valid) errors.pregnancies = pregnancies.error;
  
  // Glucose: 1-250, zero NOT allowed (biologically impossible)
  const glucose = validateNumericField(inputs.glucose, 1, 250, false);
  if (!glucose.valid) errors.glucose = glucose.error;
  
  // Blood Pressure: 1-150, zero NOT allowed
  const bloodPressure = validateNumericField(inputs.blood_pressure, 1, 150, false);
  if (!bloodPressure.valid) errors.blood_pressure = bloodPressure.error;
  
  // Skin Thickness: 0-100, zero allowed (not measured)
  const skinThickness = validateNumericField(inputs.skin_thickness, 0, 100, true);
  if (!skinThickness.valid) errors.skin_thickness = skinThickness.error;
  
  // Insulin: 0-900, zero allowed (not measured)
  const insulin = validateNumericField(inputs.insulin, 0, 900, true);
  if (!insulin.valid) errors.insulin = insulin.error;
  
  // BMI: 1-70, zero NOT allowed
  const bmi = validateNumericField(inputs.bmi, 1, 70, false);
  if (!bmi.valid) errors.bmi = bmi.error;
  
  // Diabetes Pedigree: 0.01-3.0, zero NOT allowed
  const pedigree = validateNumericField(inputs.diabetes_pedigree, 0.01, 3.0, false);
  if (!pedigree.valid) errors.diabetes_pedigree = pedigree.error;
  
  // Age: 18-120
  const age = validateNumericField(inputs.age, 18, 120, false);
  if (!age.valid) errors.age = age.error;
  
  return {
    valid: Object.keys(errors).length === 0,
    errors
  };
};

/**
 * Validate all glucose prediction inputs (regression).
 * 
 * Same as diabetes inputs but WITHOUT glucose field.
 */
export const validateGlucoseInputs = (inputs) => {
  const errors = {};
  
  const pregnancies = validateNumericField(inputs.pregnancies, 0, 20, true);
  if (!pregnancies.valid) errors.pregnancies = pregnancies.error;
  
  const bloodPressure = validateNumericField(inputs.blood_pressure, 1, 150, false);
  if (!bloodPressure.valid) errors.blood_pressure = bloodPressure.error;
  
  const skinThickness = validateNumericField(inputs.skin_thickness, 0, 100, true);
  if (!skinThickness.valid) errors.skin_thickness = skinThickness.error;
  
  const insulin = validateNumericField(inputs.insulin, 0, 900, true);
  if (!insulin.valid) errors.insulin = insulin.error;
  
  const bmi = validateNumericField(inputs.bmi, 1, 70, false);
  if (!bmi.valid) errors.bmi = bmi.error;
  
  const pedigree = validateNumericField(inputs.diabetes_pedigree, 0.01, 3.0, false);
  if (!pedigree.valid) errors.diabetes_pedigree = pedigree.error;
  
  const age = validateNumericField(inputs.age, 18, 120, false);
  if (!age.valid) errors.age = age.error;
  
  return {
    valid: Object.keys(errors).length === 0,
    errors
  };
};
