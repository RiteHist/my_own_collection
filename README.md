# Ansible Collection - my_own_namespace.my_own_collection

Documentation for the collection.

Данная коллекция тестирует мой ansible модуль, который создает текстовый файл на хосте с заданным содержимым по указанному пути.

Пример использования в play:

```---
- name: Test my own module
  hosts: localhost
  roles:
    - my_own_module_role
```
