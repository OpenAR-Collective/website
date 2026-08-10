import { defineCollection, z } from 'astro:content';
import { glob, file } from 'astro/loaders';

const faq = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/faq' }),
  schema: z.object({
    question: z.string(),
    section: z.string(),
    order: z.number(),
  }),
});

const supporters = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/supporters' }),
  schema: z.object({
    name: z.string(),
    website: z.string().url().optional(),
    logo: z.string().optional(),
  }),
});

const news = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/news' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    category: z.string(),
    image: z.string(),
    imageAlt: z.string(),
  }),
});

const policies = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/policies' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.string(),
    order: z.number(),
    adopted: z.coerce.date(),
  }),
});

const board = defineCollection({
  loader: file('./src/data/board.json'),
  schema: z.object({
    name: z.string(),
    office: z.string(),
    bio: z.string(),
    photo: z.string(),
    email: z.string().email(),
    linkedin: z.string().url(),
    order: z.number(),
  }),
});

const marks = defineCollection({
  loader: file('./src/data/marks.json'),
  schema: z.object({
    mark: z.string(),
    note: z.string(),
    order: z.number(),
  }),
});

export const collections = { faq, supporters, board, marks, news, policies };
