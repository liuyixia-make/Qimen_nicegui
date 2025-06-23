import sqlite3
import os
import json
from datetime import datetime

class QimenDBService:
    """
    奇门遁甲数据库服务类，用于存储和查询排盘信息
    """
    def __init__(self, db_path='qimen_records.db'):
        # 确保数据库目录存在
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建排盘记录表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS qimen_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,                   -- 排盘日期时间
            question TEXT,                        -- 所问事情
            notes TEXT,                           -- 笔记
            result TEXT,                          -- 结果：对/错/未知
            paipan_params TEXT,                   -- 排盘参数，JSON格式
            paipan_data TEXT,                     -- 排盘数据，JSON格式
            created_at TEXT NOT NULL              -- 创建时间
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_record(self, date, question, notes, paipan_params, paipan_data, result='未知'):
        """
        保存排盘记录
        
        参数:
            date: 排盘日期时间
            question: 所问事情
            notes: 笔记
            paipan_params: 排盘参数，字典格式
            paipan_data: 排盘数据，字典格式
            result: 结果，默认为'未知'
        
        返回:
            新记录的ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
        INSERT INTO qimen_records 
        (date, question, notes, result, paipan_params, paipan_data, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            date,
            question,
            notes,
            result,
            json.dumps(paipan_params, ensure_ascii=False),
            json.dumps(paipan_data, ensure_ascii=False),
            created_at
        ))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return record_id
    
    def update_record(self, record_id, question, notes, result=None):
        """
        更新排盘记录信息
        
        参数:
            record_id: 记录ID
            question: 所问事情
            notes: 笔记
            result: 结果（对/错/未知），如果为None则不更新
        
        返回:
            是否成功更新
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if result is not None:
            cursor.execute('''
            UPDATE qimen_records
            SET question = ?, notes = ?, result = ?
            WHERE id = ?
            ''', (question, notes, result, record_id))
        else:
            cursor.execute('''
            UPDATE qimen_records
            SET question = ?, notes = ?
            WHERE id = ?
            ''', (question, notes, record_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def get_all_records(self):
        """
        获取所有排盘记录
        
        返回:
            记录列表，按创建时间降序排序
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 使结果可以通过列名访问
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, date, question, notes, result, created_at
        FROM qimen_records
        ORDER BY created_at DESC
        ''')
        
        records = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return records
    
    def get_record_by_id(self, record_id):
        """
        根据ID获取排盘记录
        
        参数:
            record_id: 记录ID
        
        返回:
            记录详情，包括排盘数据
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, date, question, notes, result, paipan_params, paipan_data, created_at
        FROM qimen_records
        WHERE id = ?
        ''', (record_id,))
        
        row = cursor.fetchone()
        if row:
            record = dict(row)
            # 解析JSON数据
            record['paipan_params'] = json.loads(record['paipan_params'])
            record['paipan_data'] = json.loads(record['paipan_data'])
            conn.close()
            return record
        
        conn.close()
        return None
    
    def update_record_result(self, record_id, result):
        """
        更新排盘记录的结果
        
        参数:
            record_id: 记录ID
            result: 结果（对/错/未知）
        
        返回:
            是否成功更新
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE qimen_records
        SET result = ?
        WHERE id = ?
        ''', (result, record_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_record(self, record_id):
        """
        删除排盘记录
        
        参数:
            record_id: 记录ID
        
        返回:
            是否成功删除
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        DELETE FROM qimen_records
        WHERE id = ?
        ''', (record_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success 