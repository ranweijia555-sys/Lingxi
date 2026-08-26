-- Lingxi beta analytics. No tarot questions, cards, or interpretations are stored here.
create extension if not exists pgcrypto;

create table if not exists public.usage_events (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  anonymous_id_hash text not null check (char_length(anonymous_id_hash) = 64),
  session_id_hash text not null check (char_length(session_id_hash) = 64),
  reading_id_hash text check (reading_id_hash is null or char_length(reading_id_hash) = 64),
  event_name text not null check (event_name in ('reading_started', 'reading_completed', 'reading_failed')),
  spread_key text,
  reading_mode text check (reading_mode is null or reading_mode in ('draw', 'photo')),
  language text not null check (language in ('zh', 'en'))
);

create table if not exists public.reading_feedback (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  anonymous_id_hash text not null check (char_length(anonymous_id_hash) = 64),
  session_id_hash text not null check (char_length(session_id_hash) = 64),
  reading_id_hash text not null unique check (char_length(reading_id_hash) = 64),
  rating text not null check (rating in ('helpful', 'neutral', 'not_helpful')),
  comment text check (comment is null or char_length(comment) <= 500),
  spread_key text not null,
  reading_mode text not null check (reading_mode in ('draw', 'photo')),
  language text not null check (language in ('zh', 'en'))
);

create index if not exists usage_events_created_at_idx on public.usage_events (created_at desc);
create index if not exists usage_events_anonymous_idx on public.usage_events (anonymous_id_hash);
create index if not exists feedback_created_at_idx on public.reading_feedback (created_at desc);

alter table public.usage_events enable row level security;
alter table public.reading_feedback enable row level security;

-- The browser never talks to Supabase directly. Only the backend service-role key may access these tables.
revoke all on table public.usage_events from anon, authenticated;
revoke all on table public.reading_feedback from anon, authenticated;
grant insert, select on table public.usage_events to service_role;
grant insert, select on table public.reading_feedback to service_role;

create or replace view public.beta_metrics_daily
with (security_invoker = true)
as
with event_totals as (
  select
    created_at::date as day,
    count(distinct anonymous_id_hash) as unique_users,
    count(*) filter (where event_name = 'reading_started') as readings_started,
    count(*) filter (where event_name = 'reading_completed') as readings_completed,
    count(*) filter (where event_name = 'reading_failed') as readings_failed
  from public.usage_events
  group by created_at::date
), feedback_totals as (
  select
    created_at::date as day,
    count(*) as feedback_count,
    count(*) filter (where rating = 'helpful') as helpful_count,
    count(*) filter (where rating = 'neutral') as neutral_count,
    count(*) filter (where rating = 'not_helpful') as not_helpful_count
  from public.reading_feedback
  group by created_at::date
)
select
  coalesce(e.day, f.day) as day,
  coalesce(e.unique_users, 0) as unique_users,
  coalesce(e.readings_started, 0) as readings_started,
  coalesce(e.readings_completed, 0) as readings_completed,
  coalesce(e.readings_failed, 0) as readings_failed,
  coalesce(f.feedback_count, 0) as feedback_count,
  coalesce(f.helpful_count, 0) as helpful_count,
  coalesce(f.neutral_count, 0) as neutral_count,
  coalesce(f.not_helpful_count, 0) as not_helpful_count
from event_totals e
full outer join feedback_totals f using (day)
order by day desc;

revoke all on table public.beta_metrics_daily from anon, authenticated;
grant select on table public.beta_metrics_daily to service_role;
