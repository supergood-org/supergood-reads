import 'vite/modulepreload-polyfill'; // required for vite entrypoints

import { createApp, defineComponent, ref, onMounted } from 'vue';
import type { Ref } from 'vue';

import RadioCards from '@/js/components/forms/fields/RadioCards.vue';
import DeleteModal from '@/js/components/DeleteModal.vue';
import FieldWrapper from '@/js/components/forms/layout/FieldWrapper.vue';
import { parseJsonScript } from '@/js/utils/parseJsonScript';

interface InitialDataForVueStore {
  selectedMediaTypeContentType: number;
}

const RootComponent = defineComponent({
  delimiters: ['[[', ']]'],
  components: {
    'radio-cards': RadioCards,
    'field-wrapper': FieldWrapper,
    'delete-modal': DeleteModal,
  },
  setup() {
    const selectedMediaTypeContentType: Ref<number | null> = ref(null);
    const showDeleteReviewModal = ref(false);

    const openDeleteReviewModal = () => {
      showDeleteReviewModal.value = true;
    };
    const closeDeleteReviewModal = () => {
      showDeleteReviewModal.value = false;
    };

    onMounted(() => {
      /* Load initial data from django data loaded into "json_script".*/
      const initialData = parseJsonScript(
        'initialDataForVueStore',
      ) as InitialDataForVueStore;
      selectedMediaTypeContentType.value = initialData.selectedMediaTypeContentType;
    });

    return {
      selectedMediaTypeContentType,
      showDeleteReviewModal,
      openDeleteReviewModal,
      closeDeleteReviewModal,
    };
  },
});

const app = createApp(RootComponent);
app.mount('#media-form-vue-app');

export {};
