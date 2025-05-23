#!/bin/sh

# Corrige permissões (você pode ajustar para o path do banco se quiser mais específico)
chown -R 1000:1000 /app

# Executa o comando do CMD ou override do compose
exec "$@"