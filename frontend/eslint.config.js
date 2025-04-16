import js from '@eslint/js';
import globals from 'globals';
import vuePlugin from 'eslint-plugin-vue';
import vueEslintParser from 'vue-eslint-parser';

// Импортируем необходимые конфиги вручную
import vueEssential from 'eslint-plugin-vue/lib/configs/vue3-essential.js';
import vueRecommended from 'eslint-plugin-vue/lib/configs/vue3-recommended.js';

export default [
  js.configs.recommended,
  {
    files: ['**/*.vue', '**/*.js'],
    languageOptions: {
      parser: vueEslintParser,
      sourceType: 'module',
      ecmaVersion: 'latest',
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      vue: vuePlugin,
    },
    rules: {
      // Сохраняем правила из vue3-essential и vue3-recommended
      ...vueEssential.rules,
      ...vueRecommended.rules,

      'indent': ['error', 2], // Отступы в 2 пробела
      'quotes': ['error', 'single'], // Одинарные кавычки
      'semi': ['error', 'always'], // Обязательные точки с запятой

      // Только Composition API
      'vue/component-api-style': ['error', ['script-setup']],

      // Нейминг
      // -------

      // Пропсы в camelCase
      'vue/prop-name-casing': ['error', 'camelCase'],
      // Эмитсы в camelCase @myEvent="foo"
      'vue/custom-event-name-casing': ['error', 'camelCase'],
      // Компоненты в <template> в kebab-case "<my-component />"
      'vue/component-name-in-template-casing': ['error', 'kebab-case'],
      // defineProps/defineEmits пишем в самом начале скрипта, defineExpose последней строчкой
      'vue/define-macros-order': ['error', { defineExposeLast: true }],

      // Теги и их атрибуты
      // -------------------

      // Все атрибуты тегов в <template> пишем в двойных ковычках
      'vue/html-quotes': ['error', 'double', { avoidEscape: true }],
      // Правило закрытия тегов
      'vue/html-self-closing': [
        'error',
        {
          html: {
            void: 'any',
            normal: 'never',
            component: 'always',
          },
          svg: 'always',
          math: 'always',
        },
      ],
      // Закрывающий тег всегда на новой строчке
      'vue/html-closing-bracket-newline': [
        'error',
        {
          singleline: 'never',
          multiline: 'always',
          selfClosingTag: {
            singleline: 'never',
            multiline: 'always',
          },
        },
      ],
      // В самозакрывающихся тегах пробел перед закрытием
      'vue/html-closing-bracket-spacing': [
        'error',
        {
          selfClosingTag: 'always',
        },
      ],
      // Отступы в тегах
      'vue/html-indent': [
        'error',
        2,
        {
          alignAttributesVertically: true,
        },
      ],
      // Допустимое количество атрибутов для тегов на строчку
      'vue/max-attributes-per-line': [
        'error',
        {
          singleline: 3,
          multiline: 1,
        },
      ],
      // Переносить на новую строчку первый атрибут "много-аттрибутного" тега
      'vue/first-attribute-linebreak': [
        'error',
        {
          singleline: 'ignore',
          multiline: 'below',
        },
      ],
      // Переносить на новую строчку контекст и закрывающий тег в "много-аттрибутных" тегах
      'vue/multiline-html-element-content-newline': [
        'error',
        {
          ignoreWhenEmpty: true,
          ignores: ['pre', 'textarea'],
          allowEmptyLines: false,
        },
      ],
      // Тут про {{ good }}, всё остальное мимо
      'vue/no-multi-spaces': ['error'],
      'vue/mustache-interpolation-spacing': ['error'],
      'vue/no-spaces-around-equal-signs-in-attribute': ['error'],
    },
  },
];
