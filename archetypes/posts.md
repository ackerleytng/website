---
slug: "{{ substr .Name 11 }}"
title: "{{ with substr .Name 11 }}{{ replace . "-" " " | title }}{{ end }}"
date: {{ .Date }}
draft: true
---
