use edu;

CREATE TABLE edu.`user` (
	`no` INT(11) NOT NULL AUTO_INCREMENT COMMENT '번호',
	`name` VARCHAR(20) NOT NULL COMMENT '이름' COLLATE 'utf8mb4_unicode_ci',
	`email` VARCHAR(255) NOT NULL COMMENT '이메일' COLLATE 'utf8mb4_unicode_ci',
	`password` VARCHAR(255) NOT NULL COMMENT '비밀번호' COLLATE 'utf8mb4_unicode_ci',
	`gender` TINYINT(1) NULL DEFAULT NULL COMMENT '성별(0:여자, 1:남자)',
	`delYn` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '탈퇴여부(0:회원, 1: 탈퇴)',
	`regDate` DATETIME NOT NULL DEFAULT current_timestamp() COMMENT '회원등록일자',
	`modDate` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '회원정보수정일자',
	PRIMARY KEY (`no`) USING BTREE
)
COMMENT='사용자'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
;

CREATE TABLE edu.`board` (
	`no` INT(11) NOT NULL AUTO_INCREMENT COMMENT '번호',
	`title` VARCHAR(40) NOT NULL COMMENT '제목' COLLATE 'utf8mb4_unicode_ci',
	`content` VARCHAR(255) NULL DEFAULT NULL COMMENT '내용' COLLATE 'utf8mb4_unicode_ci',
	`delYn` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '삭제여부(0:활성화, 1: 비활성화)',
	`userNo` INT(11) NOT NULL COMMENT '작성자 번호(user.no)',
	`regDate` DATETIME NOT NULL DEFAULT current_timestamp() COMMENT '게시글 등록 일자',
	`modDate` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '게시글 수정 일자',
	PRIMARY KEY (`no`) USING BTREE,
	INDEX `FK_board_user` (`userNo`) USING BTREE,
	CONSTRAINT `FK_board_user` FOREIGN KEY (`userNo`) REFERENCES `user` (`no`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='게시판'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
;

CREATE TABLE edu.`login` (
	`id` VARCHAR(40) NOT NULL,
	`userNo` INT NOT NULL,
	`token` VARCHAR(255) NOT NULL,
	`regDate` DATETIME NOT NULL DEFAULT current_timestamp() COMMENT '등록일자'
)
COMMENT='로그인'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
;
