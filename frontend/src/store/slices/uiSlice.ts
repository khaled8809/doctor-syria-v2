import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UIState {
  darkMode: boolean;
  sidebarOpen: boolean;
  loading: {
    [key: string]: boolean;
  };
}

const initialState: UIState = {
  darkMode: localStorage.getItem('darkMode') === 'true',
  sidebarOpen: true,
  loading: {},
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleDarkMode: (state) => {
      state.darkMode = !state.darkMode;
      localStorage.setItem('darkMode', state.darkMode.toString());
    },
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.sidebarOpen = action.payload;
    },
    setLoading: (state, action: PayloadAction<{ key: string; value: boolean }>) => {
      state.loading[action.payload.key] = action.payload.value;
    },
  },
});

export const { toggleDarkMode, toggleSidebar, setSidebarOpen, setLoading } = uiSlice.actions;

export default uiSlice.reducer;
