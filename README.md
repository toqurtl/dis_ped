# dis_ped
## setting file
* vid_folder_path: 비디오의 kinovea 데이터가 저장된 폴더
* result_folder_path: 시뮬레이션 결과 폴더
```json
{
    "path":{
    "vid_folder_path": "D:\\OneDrive\\연구\\pandemic\\data\\ped_texas\\opposite_new",
    "result_folder_path": "D:\\inseok\\workspace\\pandemic_vid\\result\\new"
},
    "obstacles":[
        [5.15, 5.15, -8, 16],
        [-1.44, -1.44, -10, -1.2], 
        [-1.44, -1.44, 0, 6], 
        [-1.44, -1.44, 7.2, 16],
        [-1.44, 0, 7.2, 7.2],
        [0, 0, 7.2, 8.2],
        [-1.44, 0, 8.2, 8.2],
        [-1.44, 0, 0, 0],
        [0, 0, 0, 1],
        [-1.44, 0, 1, 1]
    ],

    "forces":{
        "force_save": true
    },

    "condition":{
        "simul_time_threshold": 1000
    }
}

```

## apps
### simulation
* pysocialforce 모델 기반 시뮬레이션 수행
* force_idx를 통해 원하는 힘을 적용
```bash
app_simulate.py [vid_idx] [force_idx] [setting_file_path]
```
### validate
* 실제 데이터와의 비교
* ade, social distance violence 등의 지표 계산
```bash
app_validate.py [vid_idx] [force_idx] [setting_file_path]
```

### compare
* 각 힘들에 대한 validation 값 비교
```bash
app_compare.py [vid_idx] [setting_file_path]
```

### aggregate
* 전체 vid_folder_path에 대한 validation 결과 집계
```bash
app_aggregate.py [setting_file_path]
```
