USE edu;

CREATE TABLE edu.`file` (
	`no` 				  INT 				  NOT NULL AUTO_INCREMENT COMMENT '번호',
	`origin` 		  VARCHAR(100)	NOT NULL COMMENT '원본이름',
	`ext`				  VARCHAR(3)		NOT NULL COMMENT '확장자', 
	`fileName`		VARCHAR(100)	NOT NULL COMMENT '파일이름',
	`contentType`	VARCHAR(20)		NOT NULL COMMENT '파일유형',
  `delYn`       BOOLEAN       NOT NULL DEFAULT '0' COMMENT '삭제여부(0:활성화, 1: 비활성화)',
	`regDate`     DATETIME      NOT NULL COMMENT '등록일자'	DEFAULT CURRENT_TIMESTAMP,
  `modDate`     DATETIME      NOT NULL COMMENT '수정일자' DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`no`) USING BTREE
)
COMMENT='파일'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE edu.`user` (
	`no`      INT           NOT NULL AUTO_INCREMENT COMMENT '번호',
	`name`    VARCHAR(20)   NOT NULL COMMENT '이름'    COLLATE 'utf8mb4_unicode_ci',
	`email`   VARCHAR(255)  NOT NULL COMMENT '이메일'  COLLATE 'utf8mb4_unicode_ci',
  `fileNo`  INT           NULL     COMMENT '파일 번호(file.no)',
  `gender`  BOOLEAN       NULL     DEFAULT '1' COMMENT '성별(0:여자, 1:남자)',
	`delYn`   BOOLEAN       NOT NULL DEFAULT '0' COMMENT '탈퇴여부(0:회원, 1: 탈퇴)',
	`regDate` DATETIME      NOT NULL DEFAULT current_timestamp() COMMENT '등록일자',
	`modDate` DATETIME      NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '수정일자',
	PRIMARY KEY (`no`) USING BTREE,
	INDEX `FK_user_file` (`fileNo`) USING BTREE,
	CONSTRAINT `FK_user_file` FOREIGN KEY (`fileNo`) REFERENCES `file` (`no`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='사용자'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE edu.`board` (
	`no`        INT           NOT NULL AUTO_INCREMENT COMMENT '번호',
	`title`     VARCHAR(40)   NOT NULL COMMENT '제목' COLLATE 'utf8mb4_unicode_ci',
	`content`   VARCHAR(255)  NULL DEFAULT NULL COMMENT '내용' COLLATE 'utf8mb4_unicode_ci',
	`delYn`     BOOLEAN       NOT NULL DEFAULT '0' COMMENT '삭제여부(0:활성화, 1: 비활성화)',
	`userNo`    INT           NOT NULL COMMENT '작성자 번호(user.no)',
	`regDate`   DATETIME      NOT NULL DEFAULT current_timestamp() COMMENT '등록일자',
	`modDate`   DATETIME      NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '수정일자',
	PRIMARY KEY (`no`) USING BTREE,
	INDEX `FK_board_user` (`userNo`) USING BTREE,
	CONSTRAINT `FK_board_user` FOREIGN KEY (`userNo`) REFERENCES `user` (`no`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='게시판'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
;

CREATE TABLE edu.`commant` (
	`no`        INT           NOT NULL AUTO_INCREMENT COMMENT '번호',
	`message`   VARCHAR(255)  NOT NULL COMMENT '댓글' COLLATE 'utf8mb4_unicode_ci',
	`delYn`     BOOLEAN       NOT NULL DEFAULT '0' COMMENT '삭제여부(0:활성화, 1: 비활성화)',
	`userNo`    INT           NOT NULL COMMENT '작성자 번호(user.no)',
  `boardNo`   INT           NOT NULL COMMENT '게시판 번호(board.no)',
	`regDate`   DATETIME      NOT NULL DEFAULT current_timestamp() COMMENT '등록일자',
	`modDate`   DATETIME      NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '수정일자',
	PRIMARY KEY (`no`) USING BTREE,
	INDEX `FK_commant_user` (`userNo`) USING BTREE,
	CONSTRAINT `FK_commant_user` FOREIGN KEY (`userNo`) REFERENCES `user` (`no`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	INDEX `FK_commant_board` (`boardNo`) USING BTREE,
	CONSTRAINT `FK_commant_board` FOREIGN KEY (`boardNo`) REFERENCES `board` (`no`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COMMENT='댓글'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
;

INSERT INTO edu.`user` (`name`, `email`) VALUE ('관리자', 'admin@admin.com');

COMMIT;