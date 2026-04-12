import { api } from '@/services/api';

export interface LanguageModel {
  display_name: string;
  model_name: string;
  provider: string;
}

export const LANGUAGE_MODELS_UPDATED_EVENT = 'language-models-updated';

// Cache for models to avoid repeated API calls
let languageModels: LanguageModel[] | null = null;

export const invalidateLanguageModelsCache = () => {
  languageModels = null;
};

export const notifyLanguageModelsUpdated = () => {
  invalidateLanguageModelsCache();

  if (typeof window !== 'undefined') {
    window.dispatchEvent(new Event(LANGUAGE_MODELS_UPDATED_EVENT));
  }
};

/**
 * Get the list of models from the backend API
 * Uses caching to avoid repeated API calls
 */
export const getModels = async (forceRefresh = false): Promise<LanguageModel[]> => {
  if (!forceRefresh && languageModels) {
    return languageModels;
  }
  
  try {
    languageModels = await api.getLanguageModels();
    return languageModels;
  } catch (error) {
    console.error('Failed to fetch models:', error);
    throw error; // Let the calling component handle the error
  }
};

/**
 * Get the default model (GPT-4.1) from the models list
 */
export const getDefaultModel = async (forceRefresh = false): Promise<LanguageModel | null> => {
  try {
    const models = await getModels(forceRefresh);
    return models.find(model => model.model_name === "gpt-4.1") || models[0] || null;
  } catch (error) {
    console.error('Failed to get default model:', error);
    return null;
  }
};
