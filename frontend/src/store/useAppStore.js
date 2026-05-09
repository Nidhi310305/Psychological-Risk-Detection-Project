import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

const newUserId = () => `user_${Math.random().toString(36).slice(2, 11)}`;

export const useAppStore = create(
  persist(
    (set) => ({
      userName: '',
      setUserName: (name) => set({ userName: name }),

      userId: newUserId(),

      stage1Data: {}, // { q1: "", q2: "" ... }
      stage1Result: null,
      setStage1Data: (data) => set({ stage1Data: data }),
      setStage1Result: (res) => set({ stage1Result: res }),

      stage2Data: { response: "", image_id: null, image_path: null },
      stage2Result: null,
      setStage2Data: (data) => set((state) => ({ stage2Data: { ...state.stage2Data, ...data } })),
      setStage2Result: (res) => set({ stage2Result: res }),

      stage3Data: {}, // { dass_1: 0, ... }
      stage3Result: null,
      setStage3Data: (data) => set({ stage3Data: data }),
      setStage3Result: (res) => set({ stage3Result: res }),

      finalResult: null,
      setFinalResult: (res) => set({ finalResult: res }),

      resetStore: () =>
        set({
          userName: '',
          userId: newUserId(),
          stage1Data: {},
          stage1Result: null,
          stage2Data: { response: "", image_id: null, image_path: null },
          stage2Result: null,
          stage3Data: {},
          stage3Result: null,
          finalResult: null,
        }),
    }),
    {
      name: 'mental-wellness-app-store',
      storage: createJSONStorage(() => localStorage),
    }
  )
);
