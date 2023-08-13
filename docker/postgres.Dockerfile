FROM postgres:15-alpine
# Тут в идеале из env брать но мне лень ))
# Ну а если и тебе лень можешь удалить нахуй эти healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=5 CMD [ "pg_isready", "-U", "postgres", "-d", "messenger", "-q" ]
