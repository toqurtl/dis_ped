# dis_ped
## setting file

* 실험정보
    * setting_id
    * force 종류
        * my_force_1
        * my_force_2
        * my_force_3        
    ```json
    {
        "setting_id": "5_10",
        "repulsive_force": "my_force_3"
    }
    ```
* 필요한 데이터 정보
    * vid_folder_path: 비디오의 kinovea 데이터가 저장된 폴더
    * result_folder_path: 시뮬레이션 결과 폴더
    ```json
    {
        "path":{
            "vid_folder_path": "D:\\OneDrive\\연구\\pandemic\\data\\ped_texas\\new_opposite",
            "result_folder_path": "D:\\inseok\\workspace\\pandemic_vid\\result\\0216"
        }
    }
    ```
* obstacle 위치
    ```json
    {

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
            ]
    }
    ```

* 시뮬레이션 기본정보(scene)
    * 그룹행동
    * agent 반지름
    * step_iwdth
    * max_speed_multiplier
    * tau
    * resolution
    ```json
    {
        "scene":{
        "enable_group": true,
        "agent_radius": 0.35,
        "step_width": 0.133,
        "max_speed_multiplier": 1.1,
        "tau": 0.5,
        "resolution": 10
        }
    }
    ```
* 힘 정보
    * desired_force
    * obstacle_force
    * ped_repuslive_force -> 힘 종류에 따라 세부파라미터 변경
    ```json
    {
        "forces":{
        "force_save": true,
        "set":{
            "desired_force":{
                "factor": 1.0,
                "relaxation_time": 0.5,
                "goal_threshold": 0.2
            },
            "obstacle_force":{
                "factor": 10.0,
                "sigma": 0.2,
                "threshold": 0.2
            },
            "my_force_3":{
                "factor": 1,
                "desired_distance": 2,
                "alpha": 500,
                "beta": 0.11,
                "lambda": 0.5
                }
            }        
        }
    }
    ```
* constraint/condition
    * simul_time_threshold: 시뮬레이션 끝나지 않는 상황을 처리하기 위함. 최대 시뮬레이션 step 수 지정
    ```json
    {
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
app_simulate.py [vid_idx] [setting_file_path]
```
### validate
* 실제 데이터와의 비교
* ade, social distance violence 등의 지표 계산
```bash
app_validate.py [vid_idx] [setting_file_path]
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

### visualize
* 시뮬레이션 결과(trajectory) jpg 형태로 저장
```bash
app_simulate.py [vid_idx] [setting_file_path]
```
