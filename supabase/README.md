# Supabase beta analytics setup

This database stores only anonymous product events and optional feedback. Tarot questions, cards, and interpretations remain in each visitor's browser.

1. Create a free Supabase project.
2. Open **SQL Editor**, paste `schema.sql`, and run it once.
3. Copy the Project URL and service-role key from **Project Settings → API**.
4. Add these secrets to the backend host (Render), never to Vercel or browser code:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
ANALYTICS_HASH_SALT=a-long-random-secret
```

The service-role key must remain server-side. The backend hashes anonymous browser and reading IDs before inserting rows. The `beta_metrics_daily` view summarizes daily users, reading completion, failures, and feedback.
