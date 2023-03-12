import 'vite/modulepreload-polyfill'; // required for vite entrypoints
import { createApp, defineComponent } from 'vue';
import { createPinia } from 'pinia';
import RadioCards from '@/static/js/components/RadioCards.vue';
import { useCreateReviewStore } from '@/static/js/stores';

const pinia = createPinia();

const RootComponent = defineComponent({
  delimiters: ['[[', ']]'],
  components: {
    'radio-cards': RadioCards,
  },
  setup() {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const store = useCreateReviewStore();
    return { store };
  },
  mounted() {
    const store = useCreateReviewStore();
    store.initiate();
  },
});

const app = createApp(RootComponent);
app.use(pinia);
app.mount('#review-form-vue-app');

export {};
