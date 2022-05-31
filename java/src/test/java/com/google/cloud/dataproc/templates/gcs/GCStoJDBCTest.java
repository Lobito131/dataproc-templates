/*
 * Copyright (C) 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */
package com.google.cloud.dataproc.templates.gcs;

import static com.google.cloud.dataproc.templates.gcs.GCSToJDBCConfig.GCS_JDBC_INPUT_FORMAT;
import static com.google.cloud.dataproc.templates.gcs.GCSToJDBCConfig.GCS_JDBC_INPUT_LOCATION;
import static com.google.cloud.dataproc.templates.gcs.GCSToJDBCConfig.GCS_JDBC_OUTPUT_BATCH_INSERT_SIZE;
import static com.google.cloud.dataproc.templates.gcs.GCSToJDBCConfig.GCS_JDBC_OUTPUT_DRIVER;
import static com.google.cloud.dataproc.templates.gcs.GCSToJDBCConfig.GCS_JDBC_OUTPUT_SAVE_MODE;
import static com.google.cloud.dataproc.templates.gcs.GCSToJDBCConfig.GCS_JDBC_OUTPUT_TABLE;
import static com.google.cloud.dataproc.templates.gcs.GCSToJDBCConfig.GCS_JDBC_OUTPUT_URL;
import static com.google.cloud.dataproc.templates.gcs.GCSToSpannerConfig.*;
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.google.cloud.dataproc.templates.util.PropertyUtil;
import com.google.cloud.dataproc.templates.util.ValidationUtil.ValidationException;
import jakarta.validation.ConstraintViolation;
import java.util.stream.Stream;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.ThrowingSupplier;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class GCStoJDBCTest {

  private static final Logger LOGGER = LoggerFactory.getLogger(GCStoJDBCTest.class);

  @BeforeEach
  void setUp() {
    PropertyUtil.getProperties().setProperty(GCS_JDBC_INPUT_FORMAT, "some value");
    PropertyUtil.getProperties().setProperty(GCS_JDBC_INPUT_LOCATION, "some value");
    PropertyUtil.getProperties().setProperty(GCS_JDBC_OUTPUT_DRIVER, "some value");
    PropertyUtil.getProperties().setProperty(GCS_JDBC_OUTPUT_TABLE, "some value");
    PropertyUtil.getProperties().setProperty(GCS_JDBC_OUTPUT_URL, "some value");
    PropertyUtil.getProperties().setProperty(GCS_JDBC_OUTPUT_BATCH_INSERT_SIZE, "some value");
    PropertyUtil.getProperties().setProperty(GCS_JDBC_OUTPUT_SAVE_MODE, "some value");
  }

  @Test
  void runTemplateWithValidParameters() {
    LOGGER.info("Running test: runTemplateWithValidParameters");
    assertDoesNotThrow((ThrowingSupplier<GCSToJDBC>) GCSToJDBC::of);
  }

  @ParameterizedTest
  @MethodSource("requiredPropertyKeys")
  void runTemplateWithMissingRequiredParameters(String propKey) {
    LOGGER.info("Running test: runTemplateWithInvalidParameters");
    PropertyUtil.getProperties().setProperty(propKey, "");
    ValidationException exception = assertThrows(ValidationException.class, GCSToJDBC::of);
    assertEquals(1, exception.getViolations().size());
    ConstraintViolation<?> violation = exception.getViolations().get(0);
    assertEquals("must not be empty", violation.getMessage());
  }

  static Stream<String> requiredPropertyKeys() {
    return Stream.of(
        GCS_JDBC_INPUT_FORMAT,
        GCS_JDBC_INPUT_LOCATION,
        GCS_JDBC_OUTPUT_DRIVER,
        GCS_JDBC_OUTPUT_TABLE,
        GCS_JDBC_OUTPUT_URL,
        GCS_JDBC_OUTPUT_BATCH_INSERT_SIZE,
        GCS_JDBC_OUTPUT_SAVE_MODE);
  }
}