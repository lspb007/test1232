# 基于paramiko模块， pip3 install paramiko
import requests
import paramiko


# ################## 获取今日未采集主机名 ##################
# result = requests.get('http://www.127.0.0.1:8000/assets.html')
# result = ['c1.com','c2.com']


# ################## 通过paramiko连接远程服务器，执行命令 ##################
# 创建SSH对象

class ssh_linux:
    def __init__(self, host_name, user_name, pass_wd):
        self.host_name = host_name
        self.user_name = user_name
        self.pass_wd = pass_wd

    def check_info(self):
        try:
            ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            # ssh.connect(hostname='172.19.18.31', port=22, username='root', password='bTv-6558*Yu')
            ssh.connect(hostname=self.host_name, port=22, username=self.user_name, password=self.pass_wd, timeout=3)

            # 执行命令
            cmd01 = "vmstat |sed  '1,2d'|awk '{print $15}'"
            cmd02 = "cat /proc/meminfo|sed -n '1,5p'|awk '{print $2}'"
            cmd03 = "df -h|sed '1d;/ /!N;s/\\n//;s/ \\+/ /;' |awk 'NR==1{print $5}'"

            """
            cpu使用率  wmic cpu get LoadPercentage
            内存使用率 wmic os get FreePhysicalMemory  /   wmic os get TotalVisibleMemorySize
            硬盘使用率
            服务和进程状态
            页面是否能正常访问

            """

            # 获取命令结果
            # cpu
            stdin, stdout, stderr = ssh.exec_command(cmd01)
            result = stdout.read()
            s = result.decode('GBK')
            cpu_ratio = 100 - int(s)
            # mem
            stdin, stdout, stderr = ssh.exec_command(cmd02)
            mem = stdout.readlines()
            mem_total = round(int(mem[0]) / 1024)
            mem_total_free = round(int(mem[1]) / 1024) + round(int(mem[3]) / 1024) + round(int(mem[4]) / 1024)
            mem_usage = str(round(((mem_total - mem_total_free) / mem_total) * 100))
            # disk
            stdin, stdout, stderr = ssh.exec_command(cmd03)
            disk = stdout.read()
            disk_use = int(disk.decode('GBK').replace('\n', '').replace('%', ''))

            print(disk_use)

            # 关闭连接
            ssh.close()

            print('cpu:', cpu_ratio)
            print('mem:', mem_usage)
            print('disk:', disk_use)
            # print(da03)
            data_dict = {'IP': self.host_name, 'CPU': cpu_ratio, 'MEM': mem_usage, 'DISK': disk_use, 'SYSERROR': 1}
            # print(data_dict)

        except Exception as e:
            data_dict = {'IP': self.host_name, 'CPU': '', 'MEM': '', 'DISK': '', 'SYSERROR': '连接超时，请手动巡检'}
        return data_dict
        # ##################  发送数据 ##################
        # requests.post('http://www.127.0.0.1:8000/assets.html',data=data_dict)


#
class ssh_windows:
    def __init__(self, host_name, user_name, pass_wd):
        self.host_name = host_name
        self.user_name = user_name
        self.pass_wd = pass_wd

    def check_info(self):
        try:
            ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            # ssh.connect(hostname='192.168.1.11', port=22, username='lsp', password='lsp851208')
            ssh.connect(hostname=self.host_name, port=22, username=self.user_name, password=self.pass_wd, timeout=3)

            # 执行命令

            # cmd02="cat /proc/meminfo|sed -n '1,4p'|awk '{print $2}'"
            # cmd03="df -h /|sed '1d'|awk '{print $5}'"

            """
            cpu使用率  wmic cpu get LoadPercentage
            内存使用率 wmic os get FreePhysicalMemory  /   wmic os get TotalVisibleMemorySize
            硬盘使用率
            服务和进程状态
            页面是否能正常访问

            """

            # 获取命令结果
            # cpu
            cmd01 = "wmic cpu get LoadPercentage"
            stdin, stdout, stderr = ssh.exec_command(cmd01)
            cpu_list = []
            # result_01=stdout.read().decode('GBK').strip('LoadPercentage').replace('\n', '').replace('\t', '').replace('\r', '').replace(' ','').replace('\n','').strip()
            # result_01 = stdout.read()
            # print(result_01)
            # da03 = stdout.read().strip('LoadPercentage').replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '').replace('\n', '').strip()
            # result_01=stdout.read().decode('GBK').strip('LoadPercentage').replace('\n', '').replace('\t', '').replace('\r', '').replace('\n','').strip()
            # cpu_list= result_01.split()

            da03 = str(stdout.read()).strip('b\'LoadPercentage').replace('\\n', '').replace('\\t', '').replace('\\r',
                                                                                                               '').replace(
                '\\', '').strip(' ')
            # list3 = list(da03)
            da03_re = ' '.join(da03.split())
            cpu_list = da03_re.split()

            print(cpu_list)
            statis = 0
            counts = 0
            for i in cpu_list:
                # cpu物理核心统计
                counts = counts + 1
                statis = statis + int(i)
            data03 = round(float(statis) / counts, 6)
            print("cpu use ratio: ", data03)
            # mem
            # 内存总量/Gb
            cmd04 = 'wmic memorychip get capacity'
            stdin, stdout, stderr = ssh.exec_command(cmd04)
            d4_1 = stdout.read().decode('GBK').strip('Capacity').replace(' ', '').replace('\t', '').replace('\r',
                                                                                                            '').strip()
            d4_2 = (' '.join(filter(lambda x: x, d4_1.split(' '))))
            d4_3 = d4_2.split('\n')

            counts_4 = 0
            for i in d4_3:
                counts_4 = counts_4 + int(i)

            data04 = float(counts_4) / 1024 / 1024 / 1024
            print("mem total Gb: ", data04)

            # 内存剩余量/Gb
            cmd05 = 'wmic OS get FreePhysicalMemory'
            stdin, stdout, stderr = ssh.exec_command(cmd05)
            da05 = stdout.read().decode('GBK').strip('FreePhysicalMemory').replace('\n', '').replace('\t', '').replace(
                '\r', '').replace(
                ' ', '').strip()
            data05 = round(float(da05) / 1024 / 1024, 4)
            print("mem free Gb: ", data05)

            # 内存使用率
            data06 = round(float((data04 - data05)) / data04, 4)
            mem_ratio = round(data06 * 100)
            print("mem use ratio: ", mem_ratio)

            # disk
            # 磁盘信息,根系统盘C:
            # cmd07='fsutil volume diskfree c:'
            cmd07 = 'wmic LOGICALDISK get FreeSpace,Size'
            # C盘总量
            stdin, stdout, stderr = ssh.exec_command(cmd07)
            # 删除FreeSpace,Size字符
            d7_1 = stdout.read().strip().decode('GBK').replace('FreeSpace', '').replace('Size', '')
            # 删除r-n
            d7_2 = d7_1.strip().replace('\r', '').replace('\n', '')
            # 替换多个' '为单个
            d7_3 = (' '.join(filter(lambda x: x, d7_2.split(' '))))
            # 转换str->list
            disk_data = d7_3.split(' ')
            # 获取C分区盘总量Gb,获取的数据默认单位是bytes
            data07 = round(float(disk_data[1]) / 1024 / 1024 / 1024, 4)
            print("C disk total Gb:", data07)
            # 获取C分区盘剩余量Gb
            data08 = round(float(disk_data[0]) / 1024 / 1024 / 1024, 4)
            print("C disk free Gb:", data08)
            # C分区盘使用率
            data09 = round((data07 - data08) / data07, 4)
            disk_ratio = round(data09 * 100)
            print("C disk space use ratio: ", round(data09 * 100))

            # 关闭连接
            ssh.close()

            data_dict = {'IP': self.host_name, 'CPU': data03, 'MEM': mem_ratio, 'DISK': disk_ratio, 'SYSERROR': 1}
        except Exception as e:
            data_dict = {'IP': self.host_name, 'CPU': '', 'MEM': '', 'DISK': '', 'SYSERROR': '连接超时，请手动巡检'}
        return data_dict
        # ##################  发送数据 ##################


# HP-UX服务器脚本
class ssh_hpux:
    def __init__(self, host_name, user_name, pass_wd):
        self.host_name = host_name
        self.user_name = user_name
        self.pass_wd = pass_wd

    def check_info(self):
        try:
            ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            # ssh.connect(hostname='172.19.18.31', port=22, username='root', password='bTv-6558*Yu')
            ssh.connect(hostname=self.host_name, port=22, username=self.user_name, password=self.pass_wd, timeout=3)

            # 执行命令
            cmd01 = "vmstat |sed  '1,2d'|awk '{print $18}'"
            cmd02 = "swapinfo -atm|sed 1,5d|awk '{print $5}'"
            cmd03 = "bdf / |sed 1d|awk '{print $5}'"

            """
            cpu使用率  wmic cpu get LoadPercentage
            内存使用率 wmic os get FreePhysicalMemory  /   wmic os get TotalVisibleMemorySize
            硬盘使用率
            服务和进程状态
            页面是否能正常访问

            """

            # 获取命令结果
            # cpu
            stdin, stdout, stderr = ssh.exec_command(cmd01)
            result = stdout.read()
            s = result.decode('GBK')
            cpu_ratio = 100 - int(s)

            print(cpu_ratio)
            # mem
            stdin, stdout, stderr = ssh.exec_command(cmd02)
            mem_ratio = stdout.read().decode('GBK').replace('%', '').replace('\n', '').replace('\t', '').replace('\r',
                                                                                                                 '')
            print(mem_ratio)
            # disk
            stdin, stdout, stderr = ssh.exec_command(cmd03)
            disk_ratio = stdout.read().decode('GBK').replace('%', '').replace('\n', '').replace('\t', '').replace('\r',
                                                                                                                  '')
            print(disk_ratio)

            # 关闭连接
            ssh.close()

            # print('cpu:', cpu_ratio)
            # print('mem:', mem_ratio)
            # print('disk:', disk_ratio)
            # print(da03)
            data_dict = {'IP': self.host_name, 'CPU': cpu_ratio, 'MEM': mem_ratio, 'DISK': disk_ratio, 'SYSERROR': 1}
            # print(data_dict)

        except Exception as e:
            data_dict = {'IP': self.host_name, 'CPU': '', 'MEM': '', 'DISK': '', 'SYSERROR': '连接超时，请手动巡检'}
        return data_dict
        # ##################  发送数据 ##################
        # requests.post('http://www.127.0.0.1:8000/assets.html',data=data_dict)


class ssh_other:
    def __init__(self, host_name, user_name, pass_wd):
        self.host_name = host_name
        self.user_name = user_name
        self.pass_wd = pass_wd

    def check_info(self):
        data_dict = {'IP': self.host_name, 'CPU': '', 'MEM': '', 'DISK': '', 'SYSERROR': '该系统暂不支持自动巡检'}
        return data_dict


# lsp=ssh_windows('192.168.1.11','lsp','lsp851208')
# lsp.check_info()


if __name__ == '__main__':
    sss = ssh_windows('172.19.1.79', 'administrator', 'P@ssw0rd')
    # ssh.connect(hostname='172.19.1.79', port=22, username='administrator', password='P@ssw0rd')
    # sss=ssh_windows('192.168.1.114', 'lsp007', 'btv.123')
    sss.check_info()