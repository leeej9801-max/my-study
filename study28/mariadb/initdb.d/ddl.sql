use edu;

CREATE TABLE edu.`user` (
	`no` INT(11) NOT NULL AUTO_INCREMENT COMMENT '번호',
	`name` VARCHAR(20) NOT NULL COMMENT '이름' COLLATE 'utf8mb4_unicode_ci',
	`email` VARCHAR(255) NOT NULL COMMENT '이메일' COLLATE 'utf8mb4_unicode_ci',
	`delYn` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '탈퇴여부(0:회원, 1: 탈퇴)',
	`regDate` DATETIME NOT NULL DEFAULT current_timestamp() COMMENT '회원등록일자',
	`modDate` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '회원정보수정일자',
	PRIMARY KEY (`no`) USING BTREE
)
COMMENT='사용자'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
;
