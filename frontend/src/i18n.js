import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import arTranslations from './locales/ar.json';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      ar: {
        translation: arTranslations
      }
    },
    lng: 'ar',
    fallbackLng: 'ar',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
