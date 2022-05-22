# SPEC DataCenter

Just a demo for practise.

## Backup

```sql
update dwd_test_info dwd, dim_date dim
set dwd.created_at = dim.full_date
where dwd.test_date_id = dim.id
```
```sql
alter table dwd_test_info add cpu_vendor varchar(300) default ''

update dwd_test_info dwd, dim_cpu dim
set dwd.cpu_vendor=dim.cpu_vendor
where dwd.cpu_id=dim.id
```