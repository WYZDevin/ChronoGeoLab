import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { SelectedAnchor } from '@/interfaces/map-types';

export type PrismExplorerMode = 'idle' | 'selectingA' | 'selectingB' | 'ready' | 'computing';

export interface PrismParams {
  prismMode: string;
  speedMode: string;
  customSpeed: number;
  durationMinutes: number;
  bufferMeters: number;
  timeSlices: number;
  showPPA: boolean;
  showAxes: boolean;
  timeBreaks: string;
  roadNetworkDatasetId: string;
  h3Resolution: number;
  minActivityMinutes: number;
  /**
   * Realistic-speed adjustment (road-network prism): 'off' = free-flow profile
   * speeds; 'auto' = calibrate from the GPS trajectory (fallback: time-of-day
   * congestion factor); 'manual' = multiply speeds by speedFactor.
   */
  speedAdjustment: 'off' | 'auto' | 'manual';
  /** Real speed = factor × profile speed (used when speedAdjustment='manual'). */
  speedFactor: number;
  /**
   * Optional total-time-budget override (minutes) for the road-network prism.
   * When set, it replaces the default T = t_B − t_A derived from the two
   * anchor timestamps.
   */
  totalBudgetMinutes: number;
}

interface PrismExplorerState {
  mode: PrismExplorerMode;
  anchorA: SelectedAnchor | null;
  anchorB: SelectedAnchor | null;
  params: PrismParams;
  /** Dataset/layer IDs owned by the explorer — removed on recompute or close */
  ownedDatasetIds: string[];
  ownedLayerIds: string[];
}

const initialState: PrismExplorerState = {
  mode: 'idle',
  anchorA: null,
  anchorB: null,
  params: {
    prismMode: 'road-network-stp',
    speedMode: 'walking',
    customSpeed: 5,
    durationMinutes: 45,
    bufferMeters: 100,
    timeSlices: 15,
    showPPA: true,
    showAxes: true,
    timeBreaks: 'auto',
    roadNetworkDatasetId: '',
    h3Resolution: 9,
    minActivityMinutes: 5,
    speedAdjustment: 'off',
    speedFactor: 0.7,
    totalBudgetMinutes: 30,
  },
  ownedDatasetIds: [],
  ownedLayerIds: [],
};

const prismExplorerSlice = createSlice({
  name: 'prismExplorer',
  initialState,
  reducers: {
    startExplorer(state) {
      state.mode = 'selectingA';
      state.anchorA = null;
      state.anchorB = null;
    },

    setAnchorA(state, action: PayloadAction<SelectedAnchor>) {
      state.anchorA = action.payload;
      state.mode = 'selectingB';
    },

    setAnchorB(state, action: PayloadAction<SelectedAnchor>) {
      state.anchorB = action.payload;
      state.mode = 'ready';
    },

    swapAnchors(state) {
      const tmp = state.anchorA;
      state.anchorA = state.anchorB;
      state.anchorB = tmp;
    },

    clearAnchorB(state) {
      state.anchorB = null;
      state.mode = 'selectingB';
    },

    pickNewAnchors(state) {
      state.anchorA = null;
      state.anchorB = null;
      state.mode = 'selectingA';
    },

    updateParams(state, action: PayloadAction<Partial<PrismParams>>) {
      Object.assign(state.params, action.payload);
    },

    setComputing(state) {
      state.mode = 'computing';
    },

    setReady(state) {
      state.mode = 'ready';
    },

    setOwnedIds(state, action: PayloadAction<{ datasetIds: string[]; layerIds: string[] }>) {
      state.ownedDatasetIds = action.payload.datasetIds;
      state.ownedLayerIds = action.payload.layerIds;
    },

    closeExplorer() {
      return initialState;
    },
  },
});

export const {
  startExplorer,
  setAnchorA,
  setAnchorB,
  swapAnchors,
  clearAnchorB,
  pickNewAnchors,
  updateParams,
  setComputing,
  setReady,
  setOwnedIds,
  closeExplorer,
} = prismExplorerSlice.actions;

export default prismExplorerSlice.reducer;
